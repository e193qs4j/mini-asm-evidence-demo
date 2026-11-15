import json
from dataclasses import dataclass, asdict
from typing import List
import random

@dataclass
class Asset:
    host: str
    port: int
    service: str
    evidence: str = ''

def discover(target: str) -> List[Asset]:
    ports = [(80, 'http'), (443, 'https'), (22, 'ssh')]
    assets = []
    for port, svc in ports:
        if random.random() > 0.35:
            assets.append(Asset(target, port, svc))
    return assets

def validate(asset: Asset) -> dict:
    findings = []
    if asset.service == 'http':
        asset.evidence = 'HTTP/1.1 200 OK; Server: demo-nginx'
        findings.append({'check': 'http-service', 'validated': True, 'evidence': asset.evidence})
    if asset.service == 'ssh':
        asset.evidence = 'SSH-2.0-OpenSSH_8.9'
        findings.append({'check': 'ssh-banner', 'validated': True, 'evidence': asset.evidence})
    return {'asset': asdict(asset), 'findings': findings}

def main():
    targets = ['app.example.com', 'api.example.com']
    report = {'targets': targets, 'assets': []}
    for target in targets:
        for asset in discover(target):
            result = validate(asset)
            report['assets'].append(result)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()