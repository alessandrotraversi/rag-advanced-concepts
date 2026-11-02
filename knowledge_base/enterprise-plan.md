---
title: Enterprise Plan
tenant: fcai
product: fcai-cloud
plan: enterprise
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Enterprise Plan

The FCAI Cloud **Enterprise** plan is aimed at companies with large teams, high data
volume and advanced security, governance and support requirements. This document
details the benefits, security and compliance, user and access management, onboarding,
premium support, commercial terms, SLA and the differences compared to the Starter and
Pro plans. All numbers are fictitious.

## Who Enterprise Is For

Enterprise serves organizations that:

- Have many teams and services monitored at the same time.
- Need long data retention due to internal or regulatory requirements.
- Require security controls such as SSO and RBAC.
- Need support with a shorter SLA and 24x7 coverage.
- Prefer corporate invoicing instead of card billing.
- Require centralized governance and executive reports.

## Benefits

- **Unlimited users** and an organization structured into multiple teams.
- **Configurable data retention**, of up to 15 months.
- **Ingestion volume** of metrics and logs negotiated by contract.
- **Dedicated isolated environment** available on demand.
- **Anomaly detection** and advanced alerts included.
- **Executive reports** on usage, availability and adoption.
- **Per-team quotas**, preventing one team from consuming all the capacity.

## Security and Compliance

- **Encryption** of data in transit and at rest.
- **Single Sign-On (SSO)** via SAML, integrating with the customer's identity provider.
- **Automatic user provisioning** via SCIM.
- **Role-based access control (RBAC)**, with customizable roles.
- **Audit trails** of user actions on the platform.
- **Data retention and deletion policy** configurable according to the customer's
  internal requirements.
- **Compliance reports** made available under a non-disclosure agreement.
- **Network access restriction** (IP allowlist), when applicable.

### Data Governance

Enterprise lets you define retention and masking policies for sensitive data in logs,
and control which teams have access to which data sources. These policies are
configured by the organization administrator and audited through access trails.

## User and Access Management

The Enterprise plan offers a central administration panel that allows you to:

- Create and manage multiple teams within the same organization.
- Assign roles and permissions per team and per resource.
- Provision and deprovision users automatically via SCIM.
- Define access policies, such as restriction by corporate e-mail domain.
- Query audit trails for security and governance purposes.

### Default Roles (fictitious)

- **Administrator:** manages the organization, teams, billing and security.
- **Editor:** creates and edits dashboards, alerts and integrations.
- **Analyst:** queries data and dashboards, without changing settings.
- **Read-only:** view access for stakeholders.

## Onboarding and Adoption

Enterprise customers get a fictitious assisted onboarding process that includes:

1. **Kickoff:** alignment of goals, monitoring scope and owners.
2. **Rollout:** configuration of agents, integrations and the first dashboards.
3. **Training:** training the teams on the platform.
4. **Follow-up:** periodic adoption reviews with the account manager.

### Success Plan

The account manager defines, together with the customer, a success plan with adoption
goals, rollout milestones and value indicators. Quarterly reviews assess progress and
adjust the plan as usage evolves.

## Premium Support

- **24x7** support for critical tickets.
- **Shorter SLA:** P1 with a response within 1 hour (see the support SLA document).
- **Dedicated support channel** and an emergency phone line for P1.
- **Account manager** responsible for following the account and P1 and P2 tickets.
- **Root cause report** (post-mortem) for critical incidents.

## Commercial Terms

- Commercial contract with customized terms.
- **Corporate invoicing**, with invoices issued according to the agreement.
- Volume discounts on users and ingestion.
- Negotiated payment terms and billing methods (see the billing policy).
- Renewal and adjustment clauses defined in the contract.
- Optional invoicing per cost center or business unit.

## Availability and Credits

Enterprise has a monthly availability target of **99.9%** and an SLA credit policy when
the target is not met, as detailed in the support SLA document. Credits are applied as
a discount on the next invoice.

## Differences Compared to the Starter and Pro Plans

| Aspect | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Users | 3 | up to 20 | unlimited |
| Data retention | 7 days | 30 days | up to 15 months |
| Log ingestion | 5 GB/month | 100 GB/month | by contract |
| Support | community | standard SLA | shorter SLA, 24x7 |
| SSO / RBAC / Audit | no | no | yes |
| Billing | — | card | corporate, by contract |
| Account manager | no | no | yes |
| SLA credit | no | no | yes |

In short, Enterprise stands out for scale (unlimited or widely configurable users and
retention), advanced security (SSO, RBAC and auditing), support with 24x7 coverage and
a commercial model based on a corporate contract instead of recurring card billing.

## Frequently Asked Questions

**Does Enterprise have a user limit?**
No. The plan offers unlimited users.

**How does SSO work?**
Via SAML, integrating with the customer's identity provider, with provisioning via
SCIM.

**Is there an account manager?**
Yes. Enterprise includes a dedicated account manager.

**What is the maximum data retention?**
Configurable up to 15 months, according to the contract.
