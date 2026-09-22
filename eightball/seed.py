"""Fictional, human-authored starter playbooks. Never represent these as AI-generated."""
from datetime import timedelta
from .models import Situation, Graph, utcnow


def retention_graph() -> Graph:
    conditions = [
        ('records', 'Incident records preserved', 'Preservation log reviewed by the case lead'),
        ('root', 'Root cause established', 'Technical lead signs the root-cause report'),
        ('contained', 'Immediate failure contained', 'Recovery checks and monitoring reviewed'),
        ('report', 'Remediation report approved', 'Report approved by technical lead and case lead'),
        ('authority', 'Commercial authority agreed', 'Written negotiation limits approved by the client company'),
        ('requirements', 'Customer requirements confirmed', 'Customer confirms conditions for continuing'),
        ('standstill', 'Customer grants a standstill', 'Written customer agreement to pause termination'),
        ('retained', 'Customer agrees to continue', 'Written continuation agreement accepted by both parties')]
    def a(id, title, owner, requires, produces, minutes, cost=0, risk='low', approval=False, contingent=False, purpose=None):
        return dict(id=id, title=title, owner=owner, requires=requires, produces=produces, minutes=minutes,
                    cost=cost, risk=risk, approval_required=approval, contingent=contingent, purpose=purpose or title)
    actions = [
        a('preserve', 'Preserve incident records', 'Case lead', [], ['records'], 30, 100),
        a('investigate', 'Establish the root cause', 'Technical lead', ['records'], ['root'], 180, 900),
        a('contain', 'Contain the service failure', 'Technical lead', ['records'], ['contained'], 90, 400),
        a('report', 'Prepare and approve remediation', 'Technical lead', ['root', 'contained'], ['report'], 120, 600),
        a('authority', 'Agree negotiation limits', 'Company director', [], ['authority'], 45, 100),
        a('listen', 'Confirm customer requirements', 'Account director', ['records'], ['requirements'], 45, 200, approval=True, contingent=True),
        a('pause', 'Request a written standstill', 'Account director', ['contained', 'authority'], ['standstill'], 30, 300, 'medium', True, True),
        a('direct', 'Direct recovery agreement', 'Account director', ['report', 'requirements', 'authority'], ['retained'], 60, 1000, 'medium', True, True),
        a('staged', 'Staged recovery agreement', 'Account director', ['report', 'standstill', 'authority'], ['retained'], 180, 700, 'low', True, True),
        a('mediated', 'Professionally mediated agreement', 'External mediator', ['report', 'requirements', 'authority'], ['retained'], 240, 3500, 'low', True, True),
    ]
    return Graph(conditions=[dict(id=i, title=t, confirmation=p) for i, t, p in conditions], actions=actions, goals=['retained'])


def recovery_graph() -> Graph:
    return Graph(conditions=[
        dict(id='scope', title='Service impact confirmed', confirmation='Case lead verifies the impact log'),
        dict(id='restored', title='Service restored', confirmation='Recovery checks passed and reviewed'),
        dict(id='accepted', title='Recovery accepted', confirmation='Service owner signs off monitoring results')],
        actions=[
            dict(id='scope', title='Establish incident scope', owner='Case lead', requires=[], produces=['scope'], minutes=30, cost=100, purpose='Identify affected systems and people'),
            dict(id='repair', title='Repair the affected service', owner='Technical lead', requires=['scope'], produces=['restored'], minutes=180, cost=1200, purpose='Restore the existing service'),
            dict(id='fallback', title='Activate an approved fallback', owner='Technical lead', requires=['scope'], produces=['restored'], minutes=60, cost=2500, approval_required=True, purpose='Use the reviewed continuity option'),
            dict(id='accept', title='Verify and accept recovery', owner='Service owner', requires=['restored'], produces=['accepted'], minutes=30, cost=100, contingent=True, purpose='Confirm recovery against agreed checks')], goals=['accepted'])


def create_case(title='Northstar account recovery', client='Aster Systems · fictional', summary=None,
                desired_outcome=None, template='retention', budget=7000, deadline=None) -> Situation:
    return Situation(title=title, client=client,
        summary=summary or 'A fictional major customer is considering termination following a service outage. Conflicting accounts must be checked before a recovery proposal is agreed.',
        desired_outcome=desired_outcome or ('Retain the customer with a written, accepted recovery agreement' if template == 'retention' else 'Restore service and obtain verified acceptance'),
        graph=retention_graph() if template == 'retention' else recovery_graph(), budget=budget,
        deadline=deadline or utcnow() + timedelta(hours=24))
