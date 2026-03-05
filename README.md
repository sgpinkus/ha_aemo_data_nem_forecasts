# AEMO_DATA_NEM_FORECASTS
Simple integration that takes data from a public AEMO NEM API endpoint and exposes it as many `SensorEntity` instances.
We only expose data from a single API endpoint the give 30m interval forecasts for all NEM regions - more end points might be added later.
One sensor is created for each of REGION x ("ACTUAL" | "FORECAST") x METRIC giving 5x2x6=60 possible entities grouped into device by region.

# INSTALLATION
Copy `custom_components/aemo_data_nem_forecasts/` to you local `custom_components/` directory or installd via [HACS](#).

# USAGE
**With apexcharts:** Add this to configuration.yaml (install apexcharts via HACS first) then restart:

```
resources:
  - url: /hacsfiles/apexcharts-card/apexcharts-card.js
    type: module

type: custom:apexcharts-card
header:
  title: "NSW1 RRP"
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.nsw1_rrp_actual
    name: "RRP Actual"
    type: line
    show:
      datalabels: false
    data_generator: >
      return entity.attributes.series.map(a => {
        return { x: new Date(a[0]), y: a[1] };
      });
  - entity: sensor.nsw1_rrp_forecast
    name: "RRP Forecast"
    type: line
    show:
      datalabels: false
    data_generator: >
      return entity.attributes.series.map(a => {
        return { x: new Date(a[0]), y: a[1] };
      });
```