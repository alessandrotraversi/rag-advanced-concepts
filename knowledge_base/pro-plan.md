---
title: Pro Plan
tenant: fcai
product: fcai-cloud
plan: pro
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Pro Plan

The FCAI Cloud **Pro** plan is the self-service paid plan, aimed at production teams
that need higher limits, a business-hours support SLA and predictable card billing.
This document details who the plan is for, its limits, features, security, support,
commercial terms, availability and the differences compared to the Starter and
Enterprise plans. All numbers are fictitious!

## Who Pro Is For

Pro serves organizations that:

- Already run services in production and rely on observability every day.
- Have a mid-sized engineering team, with up to 20 people on the platform.
- Need a longer data history than Starter's 7 days.
- Want a formal support response time, even if only during business hours.
- Prefer to purchase on their own, without commercial negotiation or a contract.
- Accept recurring credit card billing.

## Plan Limits

- **Up to 20 users** in the organization.
- **30-day data retention** for metrics, logs and traces.
- **100 GB of log ingestion per month**, with overage billed per GB.
- **Multiple teams** within the organization, without per-team quotas.
- **Advanced alerts** and integrations with notification channels.
- **Custom dashboards**, with no limit on quantity.

## Overage

Unlike Starter, Pro **does not pause ingestion** when the limit is reached: the volume
above the plan quota is billed as **overage**, measured per GB at the close of the
cycle.

- Notifications are sent when **80%** and **100%** of the plan quota are reached.
- The usage panel shows current consumption and projects the estimated overage for the
  cycle.
- Usage alerts can be set up to avoid surprises on the invoice.
- Overage that has already been invoiced is **non-refundable**.

### Calculation Example (fictitious)

If the organization consumes 130 GB in a cycle, the 30 GB above the 100 GB included are
billed as overage, at the current price per GB, at the close of the cycle (see the
billing policy).

## Included Features

- Collection of **metrics, logs and traces**, with correlation across the three
  pillars.
- **Distributed tracing** with configurable sampling.
- **Alerts** with multiple notification destinations.
- **Ticket portal** and **support e-mail** for opening tickets.
- **Usage panel** with consumption and overage projection for the cycle.

## Security

- **Encryption** of data in transit and at rest, the same as the other plans.
- **E-mail and password authentication**, with optional two-step verification.
- **No Single Sign-On (SSO)** and **no SCIM provisioning**.
- **No role-based access control (RBAC)** and **no audit trails**.
- No network access restriction or IP allowlist.

SSO, SCIM, RBAC, auditing and data governance policies are exclusive to the Enterprise
plan. Organizations with these requirements should consider upgrading.

## User and Access Management

- Invite up to 20 users by e-mail.
- Organize users into **teams**, to separate dashboards and alerts.
- Simplified permissions, without customizable per-resource roles.
- **Manual** provisioning and deprovisioning, without SCIM.

## Onboarding and Adoption

Pro onboarding is **self-service**, supported by the documentation:

1. **Upgrade:** direct purchase in the panel, with a credit card.
2. **Agent installation:** quick start guide and ready-made integrations.
3. **Alert setup:** alert templates for the most common services.
4. **Follow-up:** the team tracks adoption itself through the usage panel.

There is no assisted kickoff, success plan or account manager on this plan — those are
exclusive to Enterprise.

## Support

Service during **business hours**, Monday to Friday (see the support SLA document):

- **P1:** response within 8 business hours.
- **P2:** response within 1 business day.
- **P3:** response within 3 business days.

Available channels:

- **Support e-mail:** support@fcai.example.com.
- **Ticket portal:** opening and tracking tickets.
- **Knowledge base** and community.

There is no 24x7 coverage, dedicated channel, P1 emergency phone line, account manager
or root cause report — all exclusive to Enterprise.

## Commercial Terms

- **Price: R$ 499/month** with monthly billing, or **R$ 5,090/year** with yearly
  billing.
- The **yearly** subscription has a **15% discount** compared to the equivalent monthly
  price.
- **Self-service** purchase, without a commercial contract.
- **Recurring credit card billing**, with an invoice issued.
- **14-day trial** of Pro features, with no credit card required.
- **Refund** within **7 calendar days** after purchase, according to the right of
  withdrawal. After that period, there is no prorated refund.

### Upgrade and Downgrade

Upgrading from Starter is immediate, with a charge prorated to the remaining period of
the cycle. On cancellation, access remains active until the end of the cycle already
paid, on the monthly plan, or until the end of the contracted period, on the yearly
plan.

## Availability

Pro has a monthly availability target of **99.5%**, **informational and with no SLA
credit**. The credit policy is exclusive to Enterprise, whose target is 99.9%.
Availability is measured monthly, excluding scheduled maintenance windows, and reported
on the status page.

## Differences Compared to the Starter and Enterprise Plans

| Aspect | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Users | 3 | up to 20 | unlimited |
| Data retention | 7 days | 30 days | up to 15 months |
| Log ingestion | 5 GB/month | 100 GB/month | by contract |
| Overage | no (ingestion paused) | billed per GB | per contract |
| Support | community | standard SLA (business hours) | shorter SLA, 24x7 |
| SSO / RBAC / Audit | no | no | yes |
| Billing | — | card | corporate, by contract |
| Account manager | no | no | yes |
| Availability target | — | 99.5% (informational) | 99.9% (with credit) |

In short, Pro is the middle ground: production limits and a formal business-hours SLA,
while keeping the simplicity of self-service. Anyone who needs advanced security, 24x7
support, SLA credits or corporate invoicing should consider Enterprise.

## Frequently Asked Questions

**How much does the Pro plan cost?**
R$ 499/month with monthly billing or R$ 5,090/year with yearly billing, with a 15%
discount.

**How many users does Pro allow?**
Up to 20 users in the same organization.

**What is the P1 response time on Pro?**
Up to 8 business hours, during business hours, Monday to Friday.

**Does Pro have SSO?**
No. SSO, SCIM, RBAC and audit trails are exclusive to the Enterprise plan.

**What happens if I exceed the 100 GB of ingestion?**
The additional volume is billed as overage, per GB, at the close of the cycle.

**Does Pro have SLA credits?**
No. The 99.5% target is informational. SLA credits are exclusive to Enterprise.
