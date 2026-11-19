"""Review one planning cycle using its public-source evidence only."""

from datetime import datetime, timezone


def document(status):
    stamp = datetime.fromtimestamp(status['updated_at'], timezone.utc).isoformat(timespec='seconds')
    checked = status.get('website_checked_at')
    pending = status.get('pending_ideas')
    facts = status.get('public_facts') or []
    if status['status'] == 'needs_review':
        assessment = 'The planning cycle could not finish. Check the configuration before using previous campaign evidence.'
    elif status['status'] == 'stopped':
        assessment = 'The planner stopped before it finished checking proposals. The pending count covers only the proposals checked.'
    elif pending:
        assessment = f'{pending} campaign ideas await review for drafting.' if pending != 1 else 'One campaign idea awaits review for drafting.'
    elif pending == 0:
        assessment = 'The planner recorded no ideas awaiting review in this cycle.'
    else:
        assessment = 'The cycle ended without a proposal count.'
    evidence = [{'type': 'table', 'columns': ['Recorded quotation', 'Public source'],
                 'rows': [[fact['claim'], fact['source_url']] for fact in facts]}] if facts else [
                     {'type': 'paragraph', 'text': 'This snapshot contains no checked public quotations.'}]
    if checked is not None:
        evidence.append({'type': 'paragraph', 'text': 'Website evidence checked at ' +
                         datetime.fromtimestamp(checked, timezone.utc).isoformat(timespec='seconds') + '.'})
    return {'title': 'Campaign planning report', 'identity': 'Cycle snapshot · ' + stamp, 'sections': [
        {'id': 'assessment', 'title': 'Assessment', 'blocks': [{'type': 'paragraph', 'text': assessment}]},
        {'id': 'evidence', 'title': 'Evidence', 'blocks': evidence},
        {'id': 'coverage', 'title': 'Coverage and next review', 'blocks': [
            {'type': 'paragraph', 'text': 'Peer exchange status recorded for this cycle: ' + str(status.get('peer') or 'unavailable').replace('_', ' ') + '.'},
            {'type': 'paragraph', 'text': 'Review the proposed wording against the dated public quotations. Idea approval permits drafting. Sending requires a separate decision.'}]},
    ]}
