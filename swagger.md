<!-- Generator: Widdershins v4.0.1 -->

<h1 id="sports-odds-api">Sports Odds API v1</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Documentation of API for Sports Odds Integration v1.

Base URLs:

* <a href="http://localhost:8000/api">http://localhost:8000/api</a>

<h1 id="sports-odds-api-bookies">bookies</h1>

## get_bookies

<a id="opIdget_bookies"></a>

> Code samples

```shell
# You can also use wget
curl -X GET http://localhost:8000/api/bookies \
  -H 'Accept: application/json'

```

`GET /bookies`

Get all supported bookies.

> Example responses

> 200 Response

```json
[
  "string"
]
```

<h3 id="get_bookies-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Bookie names|Inline|

<h3 id="get_bookies-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="sports-odds-api-event">event</h1>

## event_list

<a id="opIdevent_list"></a>

> Code samples

```shell
# You can also use wget
curl -X GET http://localhost:8000/api/event \
  -H 'Accept: application/json'

```

`GET /event`

<h3 id="event_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|page|query|integer|false|A page number within the paginated result set.|
|page_size|query|integer|false|Number of results to return per page.|

> Example responses

> 200 Response

```json
{
  "count": 0,
  "total_pages": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "sports": "Basketball",
      "league": "NBA",
      "name": "string",
      "startTime": "2019-08-24T14:15:22Z",
      "updateTime": "2019-08-24T14:15:22Z",
      "awayName": "string",
      "homeName": "string",
      "e_id": "string",
      "english_name": "string"
    }
  ]
}
```

<h3 id="event_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="event_list-responseschema">Response Schema</h3>

Status Code **200**

*PagedEvent*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» count|integer|false|none|none|
|» total_pages|integer|false|none|none|
|» next|string(uri)¦null|false|none|none|
|» previous|string(uri)¦null|false|none|none|
|» results|[[Event](#schemaevent)]|true|none|none|
|»» id|integer|false|read-only|none|
|»» sports|string|false|none|Sports|
|»» league|string|false|none|League|
|»» name|string|true|none|Name of the event. e.g., Metropolitan Division @ Atlantic Division|
|»» startTime|string(date-time)¦null|false|none|Start time of the event|
|»» updateTime|string(date-time)¦null|false|none|Updated time|
|»» awayName|string¦null|false|none|Away team name|
|»» homeName|string¦null|false|none|Home team name|
|»» e_id|string¦null|false|none|ID of the event|
|»» english_name|string¦null|false|none|Name of the event|

#### Enumerated Values

|Property|Value|
|---|---|
|sports|Basketball|
|sports|Baseball|
|sports|Ice Hockey|
|sports|Football|
|league|NBA|
|league|MLB|
|league|NHL|
|league|NFL|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="sports-odds-api-market">market</h1>

## get_markets

<a id="opIdget_markets"></a>

> Code samples

```shell
# You can also use wget
curl -X GET http://localhost:8000/api/market \
  -H 'Accept: application/json'

```

`GET /market`

Get all supported market types.

> Example responses

> 200 Response

```json
[
  "string"
]
```

<h3 id="get_markets-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Market type names|Inline|

<h3 id="get_markets-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="sports-odds-api-selection">selection</h1>

## selection_list

<a id="opIdselection_list"></a>

> Code samples

```shell
# You can also use wget
curl -X GET http://localhost:8000/api/selection \
  -H 'Accept: application/json'

```

`GET /selection`

<h3 id="selection_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|page|query|integer|false|A page number within the paginated result set.|
|page_size|query|integer|false|Number of results to return per page.|

> Example responses

> 200 Response

```json
{
  "count": 0,
  "total_pages": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "sports": "Basketball",
      "league": "NBA",
      "name": "string",
      "startTime": "2019-08-24T14:15:22Z",
      "updateTime": "2019-08-24T14:15:22Z",
      "awayName": "string",
      "homeName": "string",
      "english_name": "string",
      "target_bookies": "string"
    }
  ]
}
```

<h3 id="selection_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="selection_list-responseschema">Response Schema</h3>

Status Code **200**

*PagedBookieLink*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» count|integer|false|none|none|
|» total_pages|integer|false|none|none|
|» next|string(uri)¦null|false|none|none|
|» previous|string(uri)¦null|false|none|none|
|» results|[[BookieLink](#schemabookielink)]|true|none|none|
|»» id|integer|false|read-only|none|
|»» sports|string|false|none|Sports|
|»» league|string|false|none|League|
|»» name|string|true|none|Name of the event. e.g., Metropolitan Division @ Atlantic Division|
|»» startTime|string(date-time)¦null|false|none|Start time of the event|
|»» updateTime|string(date-time)¦null|false|none|Updated time|
|»» awayName|string¦null|false|none|Away team name|
|»» homeName|string¦null|false|none|Home team name|
|»» english_name|string¦null|false|none|Name of the event|
|»» target_bookies|string|false|read-only|none|

#### Enumerated Values

|Property|Value|
|---|---|
|sports|Basketball|
|sports|Baseball|
|sports|Ice Hockey|
|sports|Football|
|league|NBA|
|league|MLB|
|league|NHL|
|league|NFL|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="sports-odds-api-sports">sports</h1>

## get_sports

<a id="opIdget_sports"></a>

> Code samples

```shell
# You can also use wget
curl -X GET http://localhost:8000/api/sports \
  -H 'Accept: application/json'

```

`GET /sports`

Get all supported sports types.

> Example responses

> 200 Response

```json
[
  "string"
]
```

<h3 id="get_sports-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Sports type names|Inline|

<h3 id="get_sports-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Event">Event</h2>
<!-- backwards compatibility -->
<a id="schemaevent"></a>
<a id="schema_Event"></a>
<a id="tocSevent"></a>
<a id="tocsevent"></a>

```yaml
id: 0
sports: Basketball
league: NBA
name: string
startTime: 2019-08-24T14:15:22Z
updateTime: 2019-08-24T14:15:22Z
awayName: string
homeName: string
e_id: string
english_name: string

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|sports|string|false|none|Sports|
|league|string|false|none|League|
|name|string|true|none|Name of the event. e.g., Metropolitan Division @ Atlantic Division|
|startTime|string(date-time)¦null|false|none|Start time of the event|
|updateTime|string(date-time)¦null|false|none|Updated time|
|awayName|string¦null|false|none|Away team name|
|homeName|string¦null|false|none|Home team name|
|e_id|string¦null|false|none|ID of the event|
|english_name|string¦null|false|none|Name of the event|

#### Enumerated Values

|Property|Value|
|---|---|
|sports|Basketball|
|sports|Baseball|
|sports|Ice Hockey|
|sports|Football|
|league|NBA|
|league|MLB|
|league|NHL|
|league|NFL|

<h2 id="tocS_BookieLink">BookieLink</h2>
<!-- backwards compatibility -->
<a id="schemabookielink"></a>
<a id="schema_BookieLink"></a>
<a id="tocSbookielink"></a>
<a id="tocsbookielink"></a>

```yaml
id: 0
sports: Basketball
league: NBA
name: string
startTime: 2019-08-24T14:15:22Z
updateTime: 2019-08-24T14:15:22Z
awayName: string
homeName: string
english_name: string
target_bookies: string

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|sports|string|false|none|Sports|
|league|string|false|none|League|
|name|string|true|none|Name of the event. e.g., Metropolitan Division @ Atlantic Division|
|startTime|string(date-time)¦null|false|none|Start time of the event|
|updateTime|string(date-time)¦null|false|none|Updated time|
|awayName|string¦null|false|none|Away team name|
|homeName|string¦null|false|none|Home team name|
|english_name|string¦null|false|none|Name of the event|
|target_bookies|string|false|read-only|none|

#### Enumerated Values

|Property|Value|
|---|---|
|sports|Basketball|
|sports|Baseball|
|sports|Ice Hockey|
|sports|Football|
|league|NBA|
|league|MLB|
|league|NHL|
|league|NFL|

