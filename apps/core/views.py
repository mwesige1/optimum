from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from apps.engagements.models import Engagement
from apps.workpapers.models import Workpaper
from apps.findings.models import Finding
from apps.accounts.models import AuditUser
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


# ============================================================
# Dashboard View
# Pulls live data from the database based on the user's role
# Partner/QC       → sees everything firm-wide
# Manager/IT       → sees their assigned engagements
# Senior/Staff/Trainee → sees only their own work
# ============================================================
@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    week_ahead = today + timedelta(days=7)

    # --------------------------------------------------------
    # Base querysets — filtered by role
    # --------------------------------------------------------
    if user.role in ['partner', 'qc']:
        # partners and QC reviewers see everything firm-wide
        engagements = Engagement.objects.all()
        findings    = Finding.objects.all()
        workpapers  = Workpaper.objects.all()

    elif user.role in ['manager', 'it_auditor']:
        # managers and IT auditors see their assigned engagements
        engagements = Engagement.objects.filter(
            lead_auditor=user
        ) | Engagement.objects.filter(
            team_members=user
        )
        engagements = engagements.distinct()
        findings    = Finding.objects.filter(
            engagement__in=engagements
        )
        workpapers  = Workpaper.objects.filter(
            engagement__in=engagements
        )

    else:
        # seniors, staff, and trainees see only their own work
        engagements = Engagement.objects.filter(
            team_members=user
        ) | Engagement.objects.filter(
            lead_auditor=user
        )
        engagements = engagements.distinct()
        findings    = Finding.objects.filter(
            raised_by=user
        ) | Finding.objects.filter(
            assigned_to=user
        )
        findings    = findings.distinct()
        workpapers  = Workpaper.objects.filter(
            prepared_by=user
        )

    # --------------------------------------------------------
    # Top stats cards
    # --------------------------------------------------------
    total_engagements = engagements.filter(
        status__in=['planning', 'fieldwork', 'reporting']
    ).count()

    total_open_findings = findings.filter(
        status__in=['open', 'in_progress']
    ).count()

    total_workpapers = workpapers.count()

    total_team = AuditUser.objects.filter(
        firm=user.firm,
        is_active=True
    ).count()

    # --------------------------------------------------------
    # Finding statistics — High / Medium / Low breakdown
    # --------------------------------------------------------
    open_findings    = findings.filter(status__in=['open', 'in_progress'])
    high_findings    = open_findings.filter(risk_level='high').count()
    medium_findings  = open_findings.filter(risk_level='medium').count()
    low_findings     = open_findings.filter(risk_level='low').count()
    overdue_findings = [f for f in open_findings if f.is_overdue()]
    overdue_count    = len(overdue_findings)

    # --------------------------------------------------------
    # Engagement progress
    # For each active engagement calculate % workpapers signed off
    # --------------------------------------------------------
    active_engagements = engagements.filter(
        status__in=['planning', 'fieldwork', 'reporting']
    ).select_related('client')[:5]

    engagement_progress = []
    for eng in active_engagements:
        total_wp  = eng.workpapers.count()
        signed_wp = eng.workpapers.filter(status='signed_off').count()
        if total_wp > 0:
            progress = int((signed_wp / total_wp) * 100)
        else:
            progress = 0
        engagement_progress.append({
            'engagement': eng,
            'total_wp':   total_wp,
            'signed_wp':  signed_wp,
            'progress':   progress,
        })

    # --------------------------------------------------------
    # Upcoming deadlines — due within 7 days
    # --------------------------------------------------------
    upcoming_findings = findings.filter(
        due_date__gte=today,
        due_date__lte=week_ahead,
        status__in=['open', 'in_progress']
    ).select_related('engagement').order_by('due_date')[:5]

    upcoming_engagements = engagements.filter(
        end_date__gte=today,
        end_date__lte=week_ahead,
        status__in=['planning', 'fieldwork', 'reporting']
    ).select_related('client').order_by('end_date')[:5]

    # --------------------------------------------------------
    # Recent findings — last 5
    # --------------------------------------------------------
    recent_findings = findings.select_related(
        'engagement', 'raised_by'
    ).order_by('-created_at')[:5]

    # --------------------------------------------------------
    # Recent workpapers — last 5
    # --------------------------------------------------------
    recent_workpapers = workpapers.select_related(
        'engagement', 'prepared_by'
    ).order_by('-created_at')[:5]

    # --------------------------------------------------------
    # Risk overview — calculated from open findings
    # --------------------------------------------------------
    total_open = open_findings.count()
    if total_open > 0:
        inherent_risk  = min(int((high_findings / total_open) * 100), 100)
        control_risk   = min(int((medium_findings / total_open) * 100), 100)
        detection_risk = min(int((low_findings / total_open) * 100), 100)
    else:
        inherent_risk  = 0
        control_risk   = 0
        detection_risk = 0

    # overall risk level label
    if high_findings > 0:
        overall_risk = 'High'
        risk_class   = 'danger'
    elif medium_findings > 0:
        overall_risk = 'Moderate'
        risk_class   = 'warning'
    else:
        overall_risk = 'Low'
        risk_class   = 'success'

    return render(request, 'core/dashboard.html', {
        # stats
        'total_engagements':   total_engagements,
        'total_open_findings': total_open_findings,
        'total_workpapers':    total_workpapers,
        'total_team':          total_team,

        # finding stats
        'high_findings':   high_findings,
        'medium_findings': medium_findings,
        'low_findings':    low_findings,
        'overdue_count':   overdue_count,

        # engagement progress
        'engagement_progress': engagement_progress,

        # deadlines
        'upcoming_findings':    upcoming_findings,
        'upcoming_engagements': upcoming_engagements,

        # recent items
        'recent_findings':  recent_findings,
        'recent_workpapers': recent_workpapers,

        # risk overview
        'inherent_risk':  inherent_risk,
        'control_risk':   control_risk,
        'detection_risk': detection_risk,
        'overall_risk':   overall_risk,
        'risk_class':     risk_class,

        # context
        'today': today,
    })


# ============================================================
# Staff Directory View
# Shows all staff members with their stats and assignments
# Partners/QC      → see all staff firm-wide
# Managers/IT      → see all staff (they manage teams)
# Senior/Staff/Trainee → see the full directory (read only)
# ============================================================
@login_required
def staff_directory(request):
    user = request.user

    # all active users in the same firm ordered by role then name
    staff = AuditUser.objects.filter(
        firm=user.firm
    ).order_by('role', 'first_name')

    # search by name or email
    search = request.GET.get('search', '')
    if search:
        staff = staff.filter(
            first_name__icontains=search
        ) | staff.filter(
            last_name__icontains=search
        ) | staff.filter(
            email__icontains=search
        )
        staff = staff.distinct()

    # filter by role
    role_filter = request.GET.get('role', '')
    if role_filter:
        staff = staff.filter(role=role_filter)

    # build enriched data for each staff member
    staff_data = []
    for member in staff:

        # how many workpapers they have prepared
        wp_count = Workpaper.objects.filter(
            prepared_by=member
        ).count()

        # how many findings they have raised
        finding_count = Finding.objects.filter(
            raised_by=member
        ).count()

        # their current active engagements (max 3 shown)
        current_engagements = Engagement.objects.filter(
            team_members=member,
            status__in=['planning', 'fieldwork', 'reporting']
        ) | Engagement.objects.filter(
            lead_auditor=member,
            status__in=['planning', 'fieldwork', 'reporting']
        )
        current_engagements = current_engagements.distinct()[:3]

        staff_data.append({
            'member':              member,
            'wp_count':            wp_count,
            'finding_count':       finding_count,
            'current_engagements': current_engagements,
        })

    return render(request, 'core/staff_directory.html', {
        'staff_data':   staff_data,
        'search':       search,
        'role':         role_filter,
        'role_choices': AuditUser.ROLE_CHOICES,
        'total_staff':  staff.count(),
    })

# ============================================================
# Risk & Analytics Overview
# Lists all engagements with direct links to their
# risk matrix and analytics dashboard
# ============================================================
@login_required
def risk_analytics_overview(request):
    user = request.user

    # filter engagements by role
    if user.role in ['partner', 'qc']:
        engagements = Engagement.objects.all()
    elif user.role in ['manager', 'it_auditor']:
        engagements = Engagement.objects.filter(
            lead_auditor=user
        ) | Engagement.objects.filter(
            team_members=user
        )
        engagements = engagements.distinct()
    else:
        engagements = Engagement.objects.filter(
            team_members=user
        ) | Engagement.objects.filter(
            lead_auditor=user
        )
        engagements = engagements.distinct()

    engagements = engagements.select_related(
        'client', 'lead_auditor'
    ).order_by('-created_at')

    # build enriched data for each engagement
    engagement_data = []
    for eng in engagements:

        # check risk matrix status
        try:
            risk_matrix   = eng.risk_matrix
            has_risk      = True
            risk_approved = risk_matrix.is_approved
            risk_areas    = eng.risk_areas.count()
            overall_risk  = risk_matrix.overall_risk
        except Exception:
            has_risk      = False
            risk_approved = False
            risk_areas    = 0
            overall_risk  = None

        # check materiality status
        try:
            materiality     = eng.materiality_calc
            has_materiality = True
            mat_approved    = materiality.is_approved
        except Exception:
            has_materiality = False
            mat_approved    = False

        # count ratio analyses
        ratio_count = eng.ratio_analyses.count()

        engagement_data.append({
            'engagement':      eng,
            'has_risk':        has_risk,
            'risk_approved':   risk_approved,
            'risk_areas':      risk_areas,
            'overall_risk':    overall_risk,
            'has_materiality': has_materiality,
            'mat_approved':    mat_approved,
            'ratio_count':     ratio_count,
        })

    return render(request, 'core/risk_analytics.html', {
        'engagement_data': engagement_data,
        'total':           engagements.count(),
    })

# add get_object_or_404 and Q to your existing imports at the top of views.py

@login_required
def staff_detail(request, user_id):
    user = request.user

    member = get_object_or_404(AuditUser, id=user_id, firm=user.firm)

    wp_count      = Workpaper.objects.filter(prepared_by=member).count()
    finding_count = Finding.objects.filter(raised_by=member).count()

    current_engagements = Engagement.objects.filter(
        Q(team_members=member) | Q(lead_auditor=member),
        status__in=['planning', 'fieldwork', 'reporting']
    ).distinct().select_related('client')

    recent_workpapers = Workpaper.objects.filter(
        prepared_by=member
    ).select_related('engagement').order_by('-created_at')[:5]

    recent_findings = Finding.objects.filter(
        raised_by=member
    ).select_related('engagement').order_by('-created_at')[:5]

    return render(request, 'core/staff_detail.html', {
        'member':              member,
        'wp_count':            wp_count,
        'finding_count':       finding_count,
        'current_engagements': current_engagements,
        'recent_workpapers':   recent_workpapers,
        'recent_findings':     recent_findings,
        'engagement_count':    current_engagements.count(),
    })