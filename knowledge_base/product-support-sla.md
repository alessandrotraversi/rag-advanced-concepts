---
title: Product Support SLA
tenant: fcai
product: fcai-cloud
plan: all
doc_type: sla
version: 2026-01
status: published
visibility: internal
---

# Product Support SLA

This document defines the service levels (SLA) of **FCAI Cloud** support. It describes
ticket severities (P1, P2 and P3), response times per plan, support channels, the
escalation process, maintenance windows, availability targets, the SLA credit policy
and the customer's responsibilities. All deadlines and amounts are fictitious and serve
as examples for the knowledge base.

## Definitions

- **Response time:** the interval between opening the ticket and the first qualified
  response from a support analyst.
- **Workaround time:** the interval until a workaround that restores operations, even
  temporarily, is made available.
- **Resolution time:** the interval until the problem is definitively fixed.
- **Business hours:** Monday to Friday, from 9 a.m. to 6 p.m. (Brasília time), except
  national holidays.
- **24x7:** full-time service, every day, including weekends and holidays, applicable
  only to critical tickets from Enterprise customers.

## Severities

### P1 — Critical

Severity **P1** represents total service unavailability or a failure that prevents data
ingestion and visualization for the whole organization. The impact is severe and no
viable workaround exists. Examples:

- Panel completely down for all users.
- Metric and log ingestion interrupted in production.
- Alerts not firing during a real incident.
- Authentication failure preventing access for all users.

### P2 — High

Severity **P2** represents a relevant service degradation, with a possible workaround.
The impact is significant, but part of the operation still works. Examples:

- Noticeable delay in log ingestion.
- Slow dashboards and queries.
- Failure of a specific connector or integration.
- Alert notifications arriving late.

### P3 — Low

Severity **P3** represents general questions and low-impact problems, with no relevant
harm to operations. Examples:

- Configuration and platform usage questions.
- Cosmetic adjustments to dashboards.
- Improvement requests and documentation clarifications.
- Questions about instrumentation best practices.

### Classification and Reclassification

The severity is suggested by the customer when opening the ticket and validated by the
support team. If the real impact differs from what was reported, support may
reclassify the severity, explaining the reason to the customer. Tickets may be
downgraded from P1 to P2 when a workaround is applied and operations are partially
restored.

## Response Time per Plan

### Starter Plan

The Starter plan **has no guaranteed response SLA**. Service is provided through the
knowledge base and the community, with no formal deadline for P1, P2 or P3.

### Pro Plan

Service during business hours, Monday to Friday:

- **P1:** response within 8 business hours.
- **P2:** response within 1 business day.
- **P3:** response within 3 business days.

### Enterprise Plan

Service with a dedicated channel and extended coverage:

- **P1:** response within 1 hour, with 24x7 service.
- **P2:** response within 4 business hours.
- **P3:** response within 1 business day.

Enterprise **P1** and **P2** tickets are followed by the account manager.

### Summary Table

| Severity | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| P1 | no SLA | 8 business hours | 1 hour (24x7) |
| P2 | no SLA | 1 business day | 4 business hours |
| P3 | no SLA | 3 business days | 1 business day |

## Support Channels

- **Knowledge base:** available for all plans, including Starter.
- **Support e-mail:** support@fcai.example.com, for the Pro and Enterprise plans.
- **Ticket portal:** opening and tracking tickets for Pro and Enterprise.
- **Dedicated channel:** available for Enterprise, with direct contact with the support
  team and the account manager.
- **Emergency phone line:** available for Enterprise P1 tickets, 24x7.

## Escalation Process

1. The ticket is opened and classified by severity by the customer.
2. The support team validates the severity and starts working within the SLA.
3. **P1** tickets are escalated immediately to the on-call team.
4. If the workaround time is not met, the ticket is escalated to support leadership
   and, on Enterprise, communicated to the account manager.
5. After resolution, the customer receives a summary of the service; for P1, a root
   cause report (post-mortem) is prepared.

### Communication During Incidents

During P1 incidents, FCAI publishes updates on the status page and, for Enterprise,
sends direct communications to the account manager. Updates happen at regular
intervals until the service is back to normal.

## Maintenance Windows

Scheduled maintenance is announced at least **72 hours** in advance by e-mail and on
the status page. Whenever possible, it happens during low-usage windows. Emergency
maintenance may happen without prior notice in critical security or stability
situations, and is communicated as soon as possible.

## Availability (Uptime)

FCAI maintains a monthly availability target of:

- **99.9%** for the **Enterprise** plan.
- **99.5%** for the **Pro** plan (informational target, with no SLA credit).
- No formal target for the **Starter** plan.

Availability is measured monthly, excluding scheduled maintenance windows, and reported
on the status page.

## SLA Credits

Applicable exclusively to the **Enterprise** plan. If the monthly availability falls
below the contracted target, the customer may request a credit on the next invoice,
according to this fictitious table:

- Availability between 99.0% and 99.9%: credit of 5% of the prorated monthly fee.
- Availability between 98.0% and 99.0%: credit of 10%.
- Availability below 98.0%: credit of 20%.

The credit request must be made within 30 days after the reference month. The credit
is not converted into a cash refund and does not accumulate across months.

### SLA Exclusions

The following do not count as unavailability for credit purposes:

- Scheduled maintenance windows announced in advance.
- Problems caused by incorrect customer configuration.
- Failures in environments or integrations outside FCAI's control.
- Use of the platform beyond the limits of the contracted plan.

## Customer Responsibilities

For the SLA to apply, the customer must:

- Classify ticket severity correctly.
- Provide enough information to reproduce the problem.
- Keep collection agents and SDKs on supported versions.
- Use the platform according to the terms of use and the limits of the contracted plan.
- Keep support and billing contacts up to date in the panel.

## Frequently Asked Questions

**What is the P1 response time on Enterprise?**
Up to 1 hour, with 24x7 service.

**Does the Starter plan have an SLA?**
No. Starter is served by the community and the knowledge base, with no guaranteed
deadline.

**How does the SLA credit work?**
It applies to Enterprise when availability falls below the target, as a discount on the
next invoice, upon request within 30 days.

**Can the severity of a ticket be reclassified?**
Yes. Support may adjust the severity according to the real impact, explaining the
reason.
