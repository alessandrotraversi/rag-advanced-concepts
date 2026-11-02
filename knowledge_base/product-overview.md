---
title: Product Overview
tenant: fcai
product: fcai-cloud
plan: all
doc_type: product
version: 2026-01
status: published
visibility: internal
---

# Product Overview

**FCAI Cloud** is an observability platform that unifies metrics, logs and traces in a
single panel. This document describes the high-level architecture, the features per
area, the available plans, each plan's limits, the supported integrations, the main use
cases and a set of frequently asked questions. The numbers and amounts mentioned are
fictitious and serve only as examples for the knowledge base.

## Concept

Observability is the ability to understand the internal state of a system from the
data it emits. FCAI Cloud organizes that data into three pillars — metrics, logs and
traces — and adds a layer of alerts and visualization to turn raw data into quick
decisions during operations.

## High-Level Architecture

FCAI Cloud is made of three main layers:

1. **Collection:** OpenTelemetry-compatible agents and SDKs send metrics, logs and
   traces to the platform's ingestion endpoints.
2. **Processing and Storage:** incoming data is normalized, indexed and stored in
   backends optimized for time series, text search and trace correlation.
3. **Visualization and Alerts:** dashboards, data explorers and an alerting engine let
   you query, correlate and react to data in real time.

Ingestion is done per region, and the customer chooses the storage region when the
organization is created. Data retention varies according to the plan.

### Data Flow

1. The agent collects data in the customer's environment.
2. The data is sent securely to the region's ingestion endpoint.
3. The platform validates, normalizes and indexes the data.
4. The data becomes available for querying in dashboards and explorers.
5. Alert rules continuously evaluate the data and trigger notifications.

## Features per Area

### Metrics

- Collection of infrastructure (CPU, memory, disk, network) and application metrics.
- Support for custom metrics via SDK and via an OpenTelemetry-compatible protocol.
- Aggregations by tags and dimensions, with configurable granularity.
- Visualization as line, area, bar charts and heat maps.
- Query functions for rates, percentiles and moving windows.

### Logs

- Centralization of logs from multiple sources and services.
- Full-text search with filters on structured attributes.
- Log parsing and enrichment through configurable rules.
- Retention configurable according to the plan, with optional archiving.
- Pattern detection and grouping of similar logs.

### Distributed Tracing

- Tracing of requests that cross multiple services.
- Span visualization on a timeline, with bottleneck identification.
- Automatic correlation between traces, logs and metrics from the same context.
- Configurable sampling to control data volume.
- Service map showing dependencies and latencies between components.

### Alerts

- Alert rules based on thresholds, missing data and anomaly detection.
- Notifications via e-mail, Slack, Microsoft Teams, PagerDuty and generic webhooks.
- Silencing and grouping policies to reduce noise.
- Trigger history and status of each alert.
- Escalation of unacknowledged alerts within a configurable time.

### Dashboards

- Customizable panels with metric, log and trace widgets.
- Internal sharing and read-only links for stakeholders.
- Dashboard templates for common scenarios.
- Dashboard variables to filter by environment, service or region.
- Full-screen view mode for NOC and operations panels.

## Plans

FCAI Cloud is offered in three plans. The main differences are the number of users,
data retention, ingestion volume and support level.

### Starter

Free plan aimed at small teams and at evaluating the platform.

- 3 users included.
- 7-day data retention.
- Up to 5 GB of log ingestion per month.
- Up to 100 active metric time series.
- Support via community and knowledge base, with no guaranteed SLA.

### Pro

Paid plan for growing teams — R$ 499/month (fictitious price).

- Up to 20 users.
- 30-day data retention.
- Up to 100 GB of log ingestion per month.
- Up to 5,000 active metric time series.
- Tracing with configurable sampling.
- Technical support with a standard SLA during business hours.

### Enterprise

Plan for companies with advanced needs — pricing on request from sales.

- Unlimited users.
- Configurable data retention, of up to 15 months.
- Ingestion volume negotiated by contract.
- Metric time series according to the contract.
- 24x7 support with a shorter SLA and a dedicated account manager.
- Advanced security features: SSO, RBAC and audit trails.

## Ingestion Limits and Quotas

Each plan has a monthly log and metric ingestion limit, plus quotas of active time
series. The behavior when the limit is reached varies by plan:

- **Starter:** when the limit is reached, ingestion stops until the next cycle.
- **Pro:** allows additional ingestion, billed as overage per GB.
- **Enterprise:** volume is negotiated by contract, with its own overage rules.

Limits are measured per billing cycle and can be tracked in the organization's usage
panel. Notifications are sent when 80% and 100% of the quota are reached. Per-team
quotas can be configured on the Enterprise plan, preventing a single team from
consuming all the contracted capacity.

## Integrations

FCAI Cloud integrates with **OpenTelemetry**-compatible collection agents and offers
native connectors for the main environments:

- **Kubernetes:** collection of cluster, pod and node metrics, plus container logs.
- **Docker:** collection of container metrics and logs on individual hosts.
- **Cloud providers:** connectors for metrics of popular managed services.
- **Incident tools:** integration with PagerDuty and messaging channels.
- **Messaging:** Slack and Microsoft Teams for alert notifications.
- **Webhooks:** generic integration for the customer's internal systems.

Official SDKs are available for the most used backend languages, allowing manual
instrumentation when needed. Automatic instrumentation covers popular HTTP, database
and message queue libraries.

## Use Cases

- **Production monitoring:** track the health of critical services in real time.
- **Incident response:** correlate metrics, logs and traces during a failure.
- **Performance analysis:** identify bottlenecks in distributed requests.
- **Capacity and cost:** track usage trends to plan infrastructure.
- **Compliance:** retain logs for the period required by internal policies.
- **User experience:** correlate backend latency with customer impact.

### Example Scenario

During an incident, a service's latency increases. The team opens the service
dashboard, spots an error spike in the logs, follows the trace of a slow request and
finds out that an external dependency is responding slowly. With metrics, logs and
traces in the same place, the diagnosis takes minutes instead of hours.

## Roadmap (Informational)

The platform's fictitious roadmap includes improvements in anomaly detection,
collaborative dashboards and compliance reports. Dates and priorities are defined
internally and may change without notice, and do not constitute a contractual
commitment.

## Frequently Asked Questions

**Does FCAI Cloud use OpenTelemetry?**
Yes. Collection is OpenTelemetry-compatible, in addition to native connectors.

**Can I change the storage region later?**
The region is defined when the organization is created and only changes through an
assisted migration.

**What happens if I exceed the ingestion quota?**
On Starter ingestion stops; on Pro and Enterprise overage is billed.

**Is there a dashboard limit?**
There is no hard limit on dashboards; the main limits are users, retention and
ingestion, according to the plan.
