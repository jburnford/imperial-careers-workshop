"""Search Wikidata by meaning through the WikidataMCP server, without an agent.

A terminal fallback for the live grounding demo. It calls the server's MCP endpoint (the
public web form at wd-mcp.wmcloud.org/docs is rate-limited and often refuses requests).

    python3 scripts/live_search.py "Henry Trimen botanist Ceylon Peradeniya"
    python3 scripts/live_search.py --statements Q2462643
"""
import argparse
import json
import urllib.request

MCP = 'https://wd-mcp.wmcloud.org/mcp'


def call(tool, arguments):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                       'params': {'name': tool, 'arguments': arguments}}).encode()
    req = urllib.request.Request(MCP, data=body, headers={
        'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode()
    for line in text.splitlines():
        if line.startswith('data:'):
            msg = json.loads(line[5:])
            if 'error' in msg:
                raise SystemExit(msg['error'])
            content = msg['result'].get('content', [])
            raw = ''.join(c.get('text', '') for c in content)
            try:
                return json.loads(raw).get('result', raw)
            except (ValueError, AttributeError):
                return raw
    raise SystemExit('No answer from the server:\n' + text[:500])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('query', nargs='?', help='name plus a few career words')
    ap.add_argument('--statements', metavar='QID', help='show the statements of one item instead')
    ap.add_argument('-n', type=int, default=8, help='number of search results to show (default 8)')
    args = ap.parse_args()
    if args.statements:
        print(call('get_statements', {'entity_id': args.statements}))
    elif args.query:
        lines = [l for l in str(call('search_items', {'query': args.query})).splitlines() if l.strip()]
        print('\n'.join(lines[:args.n]))
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
