# AEMO_DATA_NEM_FORECASTS
This Home Assistant integration pulls data from a public AEMO NEM API endpoint that underlies the Price and Demand tab of the [NEM dashboard](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem) and exposes it as a collection `SensorEntity` instances.

The AEMO API endpoint data is like:

        [
          {
            "SETTLEMENTDATE": "2026-02-27T18:40:00",
            "REGION": "NSW1",
            "RRP": 73.23171,
            "TOTALDEMAND": 8968.00000,
            "PERIODTYPE": "ACTUAL",
            "NETINTERCHANGE": -89.57000,
            "SCHEDULEDGENERATION": 7146.28839,
            "SEMISCHEDULEDGENERATION": 1736.26161,
            "APCFLAG": 0.0
          },
          ...
        ]

  - PERIODTYPE ::= ("ACTUAL" | "FORECAST")
  - [APCFLAG](https://visualisations.aemo.com.au/aemo/nemweb/mmsdatamodelreport/electricity/mms%20data%20model%20report_files/MMS_130.htm)
  - Forecast is in 30m intervals and from now until at least 04:00 the next day.
  - A settlement time of 2026-03-07T04:00:00 means the time period [03:30, 04:00]

One sensor is created for each of REGION x PERIODTYPE x METRIC giving 5x2x6=60 possible entities grouped into device by region.

The scalar value of each sensor is the most current value (the first forecast value or latest actual value).

Each sensor also stashes a "series" field in extra attributes which is the *entire* latest time series for the given metric (!).

# INSTALLATION
Copy `custom_components/aemo_data_nem_forecasts/` to you local `custom_components/` directory or install via [HACS](#) then restart.

# USAGE
**With apexcharts:** Add this apexcharts card:

```
type: custom:apexcharts-card
header:
  title: NSW1 RRP
apex_config:
  xaxis:
    type: datetime
    min: auto
    max: auto
    tickAmount: 12
now:
  show: true
  label: now
  color: var(--primary-color)
series:
  - entity: sensor.actual_rrp_vic1
    name: RRP Actual
    type: line
    show:
      datalabels: false
    data_generator: |
      return entity.attributes.series.map(a => ({ x: new Date(a[0]), y: a[1] })).slice(-48);
  - entity: sensor.forecast_rrp_vic1
    name: RRP Forecast
    type: line
    show:
      datalabels: false
    data_generator: |
      return entity.attributes.series.map(a => ({ x: new Date(a[0]), y: a[1] }));
```