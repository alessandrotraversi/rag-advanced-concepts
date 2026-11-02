---
title: Billing Policy
tenant: fcai
product: fcai-cloud
plan: all
doc_type: policy
version: 2026-01
status: published
visibility: internal
---

# Billing Policy

This document describes the payment methods of **FCAI Cloud**, the billing cycles,
overage billing, invoice issuance, how billing failures are handled, the access
restoration process, data retention after suspension and the refund rules. All amounts
and deadlines are fictitious and serve as examples.

## Billing Principles

- Predictable billing, with clear amounts and cycles before purchase.
- Usage notifications before any overage charge.
- Data and settings are preserved during the restoration period.
- Access is restored automatically once outstanding payments are settled.

## Payment Methods

### Credit Card

The **Pro** plan is billed to a credit card on a recurring basis, monthly or yearly.
Payment confirmation is immediate, and access remains active as long as the payment is
approved. The customer can update the card details at any time in the billing panel.
Keeping a backup card is recommended to avoid interruptions.

### Bank Slip (Boleto)

Companies may choose a **bank slip (boleto)** for yearly subscriptions. Main rules:

- Bank slip clearing can take up to **3 business days**.
- A new cycle is only issued once the previous payment is confirmed.
- Overdue bank slips must be reissued in the billing portal.

### Corporate Payment (Enterprise)

On the **Enterprise** plan, payment is corporate, invoiced according to the contract.
Conditions include:

- Invoices issued according to the commercial agreement.
- Negotiated payment terms (for example, 15, 30 or 45 days).
- Optional invoicing per cost center or per business unit.
- Invoices sent to the registered billing contacts.

## Billing Cycles

- **Monthly:** the charge happens on the subscription anniversary date, every month.
- **Yearly:** the charge happens once every 12 months, with a discount compared to
  monthly billing.
- **Enterprise:** the cycle is defined in the contract and can be monthly, quarterly or
  yearly.

The cycle start date is the activation date of the paid plan. Plan changes may generate
a prorated charge, according to the commercial policy.

## Overage Billing

On the **Pro** and **Enterprise** plans, the ingestion volume that exceeds the plan
limit is billed as **overage**:

- Overage is measured per **GB** of ingestion, at the close of each cycle.
- The usage panel shows current consumption and projects the estimated overage for the
  cycle.
- Notifications are sent when **80%** and **100%** of the plan quota are reached.
- On **Enterprise**, overage rules and prices follow the contract.

Overage that has already been invoiced is non-refundable. Usage alerts can be set up to
avoid surprises on the invoice.

### Calculation Example (fictitious)

If the Pro plan includes 100 GB of log ingestion and the organization consumes 130 GB in
the cycle, the additional 30 GB are billed as overage, at the current price per GB, at
the close of the cycle.

## Taxes and Invoices

- Published prices may not include taxes, which are applied according to current
  legislation and the billing address.
- An **invoice** is issued for every charge and made available in the billing portal.
- Corporate customers can configure specific tax details, such as legal name, CNPJ
  (Brazilian company tax ID) and billing address.
- Tax detail changes must be made before the cycle closes to appear on that period's
  invoice.

## Billing Failure

When a charge fails — because the card was declined, the bank slip was not paid or a
corporate invoice is overdue — FCAI follows this fictitious flow:

1. **Notification:** the billing contact is notified by e-mail about the failure.
2. **Retry:** card charges are automatically retried up to **3 times**, a few days
   apart.
3. **Grace period:** the account remains active during a grace period for settlement.
4. **Access restriction:** if the payment is still outstanding, the account enters
   restricted mode.

## Restricted Mode and Suspension

While a payment is outstanding, the account may enter **restricted mode**, with:

- Ingestion of new data **suspended**.
- **Read-only** access to the data still retained.
- Alerts and integrations paused.

If the outstanding payment is not resolved in time, the account may be **suspended**
and, after an additional period, data may be removed according to the retention
policy.

### Timeline (fictitious)

- **Day 0:** billing failure and notification.
- **Days 1 to 7:** grace period, account active.
- **Day 8:** restricted mode, ingestion suspended.
- **Day 30:** account suspension.
- **Day 60:** possible data removal according to retention.

The deadlines above are illustrative and may vary by plan and contract.

## Access Restoration

After the outstanding payment is confirmed:

- Access is restored **automatically**, with no need for a new subscription.
- Settings, dashboards and integrations are preserved, as long as the account has not
  been removed.
- Data ingestion resumes from the moment of settlement; data from the suspension period
  may not be recoverable.

## Data Retention and Deletion

After cancellation or definitive suspension, data enters a retention process and is
then deleted according to the current policy. Enterprise customers may request a data
export before deletion, within the period set in the contract.

## Refunds and Credits

- **Pro** plan refunds follow the commercial policy: up to **7 calendar days** after
  purchase.
- **SLA credits** (Enterprise) are applied to the next invoice and are not converted
  into cash (see the support SLA document).
- Billing errors are corrected on the next invoice or through a credit note, as
  appropriate.

## Frequently Asked Questions

**What happens if my card fails?**
You are notified and the charge is retried up to 3 times before access is restricted.

**Do I lose my data if the account is suspended?**
During restricted mode the data is read-only; removal only happens after the
suspension and retention periods.

**Can I get an invoice?**
Yes. An invoice is issued for every charge and is available in the billing portal.

**How do I avoid overage charges?**
Monitor the usage panel and configure usage alerts at 80% and 100% of the quota.
