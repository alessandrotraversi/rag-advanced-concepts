---
title: Starter Plan
tenant: fcai
product: fcai-cloud
plan: starter
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Starter Plan

The FCAI Cloud **Starter** plan is the platform's free entry point, aimed at small
teams, individual projects and proofs of concept. This document details who the plan
is for, its limits, included features, security, support, commercial terms,
availability and the differences compared to the Pro and Enterprise plans. All numbers
are fictitious.

## Who Starter Is For

Starter serves organizations and individuals who:

- Are evaluating FCAI Cloud before purchasing a paid plan.
- Monitor few services, usually a development environment or a single project.
- Tolerate short data retention and have no regulatory history requirement.
- Do not need a support SLA with a guaranteed deadline.
- Prefer an autonomous setup, with no contract and no credit card.

## Plan Limits

- **Up to 3 users** in the organization.
- **7-day data retention** for metrics, logs and traces.
- **Up to 5 GB of log ingestion per month**, with no overage billing.
- **A single team** within the organization, with no team separation.
- **Basic alerts** by e-mail, with no anomaly detection.
- **Default platform dashboards**, with limited customization.

When the ingestion limit is reached, the collection of new data is paused until the
next cycle. Starter **does not generate overage charges**: instead of billing the
overage, the platform stops ingestion, as a way of keeping the plan free.

## Included Features

- Collection of **metrics, logs and traces** by the default agents.
- Metric and log **explorers** for querying and filtering.
- **Integrations** with the data sources supported by the platform.
- **Status page** and public knowledge base.
- **Usage notifications** when approaching the plan's ingestion limit.

## Security

- **Encryption** of data in transit and at rest, the same as the other plans.
- **E-mail and password authentication**, with optional two-step verification.
- **No Single Sign-On (SSO)** and **no SCIM provisioning**.
- **No role-based access control (RBAC)** and **no audit trails**.
- No network access restriction or IP allowlist.

Organizations that require SSO, RBAC or auditing should consider the Enterprise plan,
which concentrates the advanced security features.

## User and Access Management

Starter offers simplified user management:

- Invite up to 3 users by e-mail.
- All users share the same access level to the organization.
- There are no customizable roles or per-resource permissions.
- Users are removed manually by the organization's creator.

## Onboarding and Adoption

Starter onboarding is **self-service**, with no involvement of the sales team:

1. **Sign-up:** create the organization directly on the website, with no credit card.
2. **Agent installation:** quick start guide in the knowledge base.
3. **First dashboard:** ready-made templates for the most common services.
4. **Community:** questions are answered in the public forum and the documentation.

There is no assisted kickoff, dedicated training or account manager on this plan.

## Support

- Service through the **knowledge base** and the **community**.
- **No guaranteed response SLA** for P1, P2 or P3 (see the support SLA document).
- **No support e-mail** and **no ticket portal**, available starting with Pro.
- No dedicated channel, emergency phone line or account manager.

## Commercial Terms

- **Price: R$ 0/month.** The plan is free indefinitely.
- **No contract** and **no credit card** required to use the plan.
- No invoices are issued, since there is no charge.
- Upgrading to Pro can be done at any time, self-service.
- At the end of the Pro plan's **14-day trial**, an organization that does not upgrade
  automatically returns to the Starter limits.

### Returning from the Trial to Starter

When the organization goes back from the Pro trial to Starter, data that exceeds the
Starter limits — such as retention beyond 7 days — may be archived or removed according
to the retention policy described in the commercial policy.

## Availability

Starter **has no formal availability target** and no SLA credit policy. The platform
runs on the same infrastructure standard as the other plans, but with no contractual
availability commitment for this plan.

## Differences Compared to the Pro and Enterprise Plans

| Aspect | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Users | 3 | up to 20 | unlimited |
| Data retention | 7 days | 30 days | up to 15 months |
| Log ingestion | 5 GB/month | 100 GB/month | by contract |
| Overage | no (ingestion paused) | billed per GB | per contract |
| Support | community | standard SLA | shorter SLA, 24x7 |
| SSO / RBAC / Audit | no | no | yes |
| Billing | — | card | corporate, by contract |
| Availability target | — | 99.5% (informational) | 99.9% |

In short, Starter trades guarantees for simplicity: it is free and immediate, but has
no SLA, no billable overage and short retention. Pro adds a business-hours SLA and
higher limits; Enterprise adds advanced security, 24x7 support and a corporate
contract.

## Frequently Asked Questions

**Is Starter free forever?**
Yes. The plan costs R$ 0/month and requires neither a credit card nor a contract.

**How many users does Starter allow?**
Up to 3 users in the same organization.

**Does Starter have a support SLA?**
No. Service is provided by the community and the knowledge base, with no guaranteed
deadline for P1, P2 or P3.

**What happens if I exceed the 5 GB of ingestion?**
Ingestion of new data is paused until the next cycle. There is no overage billing on
Starter.

**How long is data available?**
For 7 days. Longer retention requires the Pro or Enterprise plan.
