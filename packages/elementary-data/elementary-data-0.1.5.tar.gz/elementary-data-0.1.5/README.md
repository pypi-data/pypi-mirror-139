<p align="center">
<img alt="Logo" src="static/logo_elementary.png"/ width="600">
</p>

<p align="center">
<a href="https://join.slack.com/t/elementary-community/shared_invite/zt-uehfrq2f-zXeVTtXrjYRbdE_V6xq4Rg"><img src="https://img.shields.io/badge/join-Slack-orange"/></a>
<img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-brightgreen"/>
<img alt="Downloads" src="https://static.pepy.tech/personalized-badge/elementary-lineage?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads"/>
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/elementary-data/elementary-lineage?color=ff69b4"/>
</p>


Our goal is to provide data teams with **immediate visibility, detection of data issues, and impact analysis.**</br>
We focus on providing a **simple setup**, **integrations** with the existing stack, and **centralized metadata** in your own data warehouse.

## Supported use cases

**Live data lineage** - Enriched with operational context like freshness, volume, duration.

**Source tables monitoring** - Detect breaking changes and discover new data you can leverage in your source tables. 

**Alerts** - Slack alerts on breaking changes and new data can be configured within minutes.


:star: Support us with a <a href="https://github.com/elementary-data/elementary-lineage/stargazers"><img src="static/star_github.png" width="40"/></a> :star:

<img src="static/elementary_demo.gif" width="750"/>


## Demo & sandbox
Try out our live lineage [sandbox here](https://www.elementary-data.com/live-demo).


## Quick start

**Install & connect**

```bash
pip install elementary-data

# The tool is named edr (Elementary Data Reliability),
# run it to validate the installation:
edr --help
```

Add your data warehouse connection details in a `profiles.yml` file, see our [quickstart page](https://docs.elementary-data.com/quickstart) to learn more or use [this template here](static/profiles.yml). Yes, if you are a dbt user we use dbt's profiles.yml by default (simply add a new profile called 'elementary').

**Data lineage**

```bash

# Generate data lineage graph
edr lineage 

# Filter the graph for a specific table, direction and depth
edr lineage -t +my_table+3

```

**Data monitoring**


After you [configure sources to monitor](https://docs.elementary-data.com/guides/sources-monitoring/configure-datasets-to-monitor), execute it using:
```bash
edr monitor
```

To learn how to continuously monitor your data and use our Slack integration refer to our [documentation](https://docs.elementary-data.com/). 

<img alt="Slack" src="static/slack_alert.png" width="500">


## Documentation

Want to learn more on how to quickly get started with it? 
Go to our [quickstart page](https://docs.elementary-data.com/quickstart).</br>

Have questions about the configuration? 
Go to our [configuration FAQ here](https://docs.elementary-data.com/guides/connection-profile).</br>

Curious to learn about the different modules?
Use this [modules overview](https://docs.elementary-data.com/guides/modules-overview).</br>


Our full documentation is [available here](https://docs.elementary-data.com/). 

## Features

**Data lineage**
* **Lineage visualization**: Visual map of data flow and dependencies in the data warehouse, including legacy that is not managed by dbt. 
* **Dataset status**: Present data about freshness, volume, permissions and more on the lineage graph itself.
* **Accuracy**: Reflects the actual state in the DWH based on logs and your query history.
* **Plug-and-play**: No need for code changes.
* **Graph filters**: Filter the graph by dataset, dates, direction, and depth. 

**Tables monitoring**
* **Slack notifications**.
* **Detect deletions:** columns and tables that were removed.
* **Detect data type** changes.
* **Detect new data:** columns and tables that were added.

**You can impact our next features in this [roadmap](https://github.com/elementary-data/elementary-lineage/projects/1)** by voting :+1: to issues and opening new ones.

We aim to build an open, transparent, and community-powered data observability platform.
A solution that data teams could easily integrate into their workflows, detect data incidents and prevent them from even happening in the first place.

## Community & Support

For additional information and help, you can use one of these channels:

* [Slack](https://join.slack.com/t/elementary-community/shared_invite/zt-uehfrq2f-zXeVTtXrjYRbdE_V6xq4Rg) \(Live chat with the team, support, discussions, etc.\)
* [GitHub issues](https://github.com/elementary-data/elementary-lineage/issues) \(Bug reports, feature requests)
* [Roadmap](https://github.com/elementary-data/elementary-lineage/projects/1) \(Vote for features and add your inputs)
* [Twitter](https://twitter.com/ElementaryData) \(Updates on new releases and stuff)

## **Integrations**

* [x] **Snowflake** ![](static/snowflake-16.png) - Lineage & monitoring
* [x] **BigQuery**  ![](static/bigquery-16.png) - Lineage only
* [ ] **Redshift**  ![](static/redshift-16.png) 

Ask us for integrations on [Slack](https://join.slack.com/t/elementary-community/shared_invite/zt-uehfrq2f-zXeVTtXrjYRbdE_V6xq4Rg) or as a [GitHub issue](https://github.com/elementary-data/elementary-lineage/issues/new).

## **License**

Elementary is licensed under Apache License 2.0. See the [LICENSE](https://github.com/elementary-data/elementary-lineage/blob/master/LICENSE) file for licensing information.
