## Endpoints

### Staging Endpoint -> `https://c19-vac-rnd-dash-staging-api.herokuapp.com`

### Production Endpoint -> `https://c19-vac-rnd-dash-api.herokuapp.com` 


## Routes

### Ingest 
Ingest will take url, and parse csvs to load data into the database.

#### ROUTE: `/ingest`
#### METHOD: POST 
```json
{
    "source":"<url>.csv",
    "category":"trial" or "product"
    (optional) "loader":'unfiltered_csv' 
}
```
> Do not use optional loader or any other kwargs with NoneType.  That could break assignment or cause unknown loading behavior.


### Vaccines

#### ROUTE: `/vaccines`
#### METHOD: GET 
#### OUTPUT: 

```json
[
  {
    "countries": "china",
    "data_reference": null,
    "data_source": "http://www.chictr.org.cn/showproj.aspx?proj=49217",
    "enrollment_date": "Sat, 01 Feb 2020 00:00:00 GMT",
    "intervention": "no intervention",
    "intervention_type": "prognosis",
    "phase": "not applicable",
    "phase_num": null,
    "recruitment_status": "not recruiting",
    "registration_date": "Mon, 17 Feb 2020 00:00:00 GMT",
    "registry": "chictr",
    "results_link": "no results",
    "sponsors": "zhongnan hospital of wuhan university",
    "start_date": null,
    "title": "construction and analysis of prognostic predictive model of novel coronavirus pneumonia (covid-19)",
    "trial_id": "chictr2000029953"
  },
  ...
]
```



### Alternatives

#### ROUTE: `/alternatives`
#### METHOD: GET 
#### OUTPUT: 

```json
[
    {
        "countries": "china",
        "data_reference": null,
        "data_source": "http://www.chictr.org.cn/showproj.aspx?proj=49217",
        "enrollment_date": "Sat, 01 Feb 2020 00:00:00 GMT",
        "intervention": "no intervention",
        "intervention_type": "prognosis",
        "phase": "not applicable",
        "phase_num": null,
        "recruitment_status": "not recruiting",
        "registration_date": "Mon, 17 Feb 2020 00:00:00 GMT",
        "registry": "chictr",
        "results_link": "no results",
        "sponsors": "zhongnan hospital of wuhan university",
        "start_date": null,
        "title": "construction and analysis of prognostic predictive model of novel coronavirus pneumonia (covid-19)",
        "trial_id": "chictr2000029953"
    },
    ...
]
```



### Treatments

#### ROUTE: `/treatments`
#### METHOD: GET 
#### OUTPUT: 

```json
[
  {
    "countries": "china",
    "data_reference": null,
    "data_source": "http://www.chictr.org.cn/showproj.aspx?proj=49181",
    "enrollment_date": "Sun, 16 Feb 2020 00:00:00 GMT",
    "intervention": "oxygen",
    "intervention_type": "drug",
    "phase": "not applicable",
    "phase_num": null,
    "recruitment_status": "not recruiting",
    "registration_date": "Sun, 16 Feb 2020 00:00:00 GMT",
    "registry": "chictr",
    "results_link": "no results",
    "sponsors": "zhongnan hospital of wuhan university",
    "start_date": null,
    "title": "a medical records based study for the effectiveness of extracorporeal membrane oxygenation in patients with severe novel coronavirus pneumonia (covid-19)",
    "trial_id": "chictr2000029949"
  },
  ...
]
```