# sportDB

> - [表目錄](#Main-table)
> 1. [football_leagues](#football_leagues)
> 2. [football_lineups](#football_lineups)
> 3. [football_players](#football_players)
> 4. [football_team_players](#football_team_players)
> 5. [football_teams](#football_teams)
> 6. [football_technics](#football_technics)
> 7. [football_matches](#football_matches)
> 8. [football_events](#football_events)
---
- [已解決的問題](#已解決的問題)
- [其他](#other-補充)
---
- [飛鯨數據公司-連結](https://www.feijing88.com/doc?id=2-291&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Ik42c1hkeTdKZ014Q1lWVlRvSEtFQlNxYkVhS3lkczI2SERCbVZNL2tibDAzdEFrQS82UGY5WHRUckZxbG5IcDIiLCJpYXQiOjE3MzQ1ODc5Njh9.vKMtS2gUpt7Z33Z8gWBG8Dtb-LWGg9bjy18IAeUQq7w): 可幫助釐清資料的含意
- [Football API-連結](https://m.lmgoal.com/swagger/index.html?urls.primaryName=Football+API): 整理彙整後的API

## Main table

|表名|意義|欄位|
|:--------| ----------| ----------|
|[football_leagues](#football_leagues)|聯賽的中(含簡體)英文名稱和縮寫，國家、熱門、鎖定、等級|`id`, `name_en`, `name_en_short`, `name_chs`, `name_chs_short`, `name_cht`, `name_cht_short`, `type`, `sum_round`, `curr_round`, `curr_season`, `color`, `league_logo`, `league_logo_s3`, `country_id`, `is_hot`, `is_locked`, `level`|
|[football_lineups](#football_lineups)|主客場球員的組成和陣容(戰術)|`match_id`, `home_array`, `away_array`, `home_lineup`, `away_lineup`, `home_backup`, `away_backup`|
|[football_players](#football_players)|球員年齡、國籍、身價、慣用腳|`id`, `name_en`, `name_chs`, `name_cht`, `birthday`, `height`, `weight`, `nationality_id`, `photo`, `photo_s3`, `value`, `feet_en`, `feet_chs`, `feet_cht`, `nationality2_id`|
|[football_team_players](#football_team_players)|球員的位置(可能應用未知)|`team_id`, `player_id`, `position_en`, `position_chs`, `position_cht`, `number`, `end_date_contract`|
|[football_teams](#football_teams)|是否為國家隊|`league_id`, `name_en`, `name_chs`, `name_cht`, `founding_date`, `area_en`, `area_chs`, `area_cht`, `gym_en`, `gym_chs`, `gym_cht`, `capacity`, `logo`, `logo_s3`, `addr_en`, `addr_chs`, `addr_cht`, `website`, `coach_id`, `is_national`, `is_locked`|
|[football_technics](#football_technics)|技術統計|`match_id`, `technic_count`|
|[football_matches](#football_matches)|(可能應用未知)|`id`, `league_id`, `sub_league_id`, `match_time`, `start_time`, `home_id`, `away_id`, `state`, `home_score`, `away_score`, `home_half_score`, `away_half_score`, `home_red`, `away_red`, `home_yellow`, `away_yellow`, `home_corner`, `away_corner`, `home_half_red`, `away_half_red`, `home_half_yellow`, `away_half_yellow`, `home_half_corner`, `away_half_corner`, `home_rank_en`, `home_rank_chs`, `home_rank_cht`, `away_rank_en`, `away_rank_chs`, `away_rank_cht`, `is_neutral`, `has_lineup`, `has_statistics`, `group_id`, `season`, `round_en`, `round_chs`, `round_cht`, `grouping`, `location_en`, `location_chs`, `location_cht`, `weather_en`, `weather_chs`, `weather_cht`, `temp`, `extra_explain`, `is_hidden`, `injury_time`, `var`, `update_time`, `ishkjc`, `deleted`|
[football_events](#football_events)|詳細的事件是甚麼|`match_id`, `event`|

## 已解決的問題

- football_leagues
    - 總輪數、當前輪數和當前賽季可能為空值是合理的嗎?看原始資料沒看出來是怎樣的類型。
    <font color= #0000ff>$sol:$
    就只是單純的紀錄，至於對於球隊整體的評分或素質的無關 (幫助有限) $\Rightarrow$ 不太重要的資訊</font>
    > note: 盃賽也會有積分，資格$\rightarrow$附加賽$\rightarrow$聯賽。
    - 熱門的賽事是公認的嗎?
    <font color= #0000ff>$sol:$
    不是很重要的資訊，相較一般比賽較為有名。$\Rightarrow$ 不太重要的資訊</font>

    - 是否鎖定資料是甚麼意思?
    <font color= #0000ff>$sol:$
    我們會幫顧客鎖訂單(固定的賠率)，因為不希望被修改。 $\Rightarrow$ 不太重要的資訊</font>

    - 聯賽等級(分析對象) 取level 1-2 (甲乙組)
    <font color= #0000ff>$sol:$
    對於此資訊要保持高度存疑的態度，只能作為一種輔助的判斷聯賽等級的資訊，因為對方所提中的資料也有可能會抓錯。</font>

- football_players
    - nationality2_id 所代表的意義是雙重國籍嗎?還是有爭議的國籍?
    <font color= #0000ff>$sol:$
    ~~目前對此的解釋是說第一個國籍nationality_id極有可能為出生地，但是未必曾在那裏踢足球，因此這可能是發生空值的原因。第二個國籍nationality2_id為第二個國籍(雙重國籍)。~~$\Rightarrow$ 此結論尚未被證實，而空值最有可能的情況是飛鯨公司在收集的時候本身就不太完整。</font>
![alt text](附檔/image-1.png)
- football_team_players
    - position_en: 20種，猜測74404個空值，其空值的不代表是候補選手。
    <font color= #0000ff>$sol:$
    空值不一定是可能為候補選手哦，也有可能是飛鯨沒有提供數據。</font>

- football_technics
    - technic_count:不清楚內容
    <font color= #0000ff>$sol:$

> 三個為一組：
第1數字，對應那47個統計類型
第2數字，為主隊(Home)的資訊
第3數字，為客隊(away)的資訊
以此類推😊</font>

<details>
  <summary><font color=red>統計類型(點擊後展開)</font></summary>

- note:
你看到有"%" 的，通常都是 "xxx率" 的統計類型，
例如: 三個為一組，14, 53%, 47%
14：代表 控球率
53%：主隊-控球率53%
47%：客隊-控球率47% 

控球率計算方式會有不同: (1) 持球的時間長短 (2) 傳到隊友腳上的成功率-過半場, 短距離, 長距離 (3) 鏟球

----

```diff
"0,*,"表示的是主隊先開球"
技術類型：(技術統計類型int)

0.先開球
1.第一個角球
2.第一張黃牌
3.射門次數
4.射正次數
5.犯規次數
6.角球次數
7.角球次數(加時)
8.任意球次數
9.越位次數
10.烏龍球數 
11.黃牌數
12.黃牌數(加時)
13.紅牌數
14.控球率
15.頭球
16.救球
17.守門員出擊
18.丟球
19.成功搶斷
20.阻截
21.長傳
22.短傳
23.助攻
24.成功傳中
25.第一個換人
26.最後換人
27.第一個越位
28.最後越位
29.換人數
30.最後角球
31.最後黃牌
32.換人數(加時)
33.越位次數(加時)
34.射門不中
35.中柱
36.頭球成功次數
37.射門被擋
38.鏟球
39.過人次數
40.界外球
41.傳球次數
42.傳球成功率
43.進攻次數
44.危險進攻次數
45.半場角球
46.半場控球
47.撲出點球。
```
</details>
<br>

$\blue\bigstar$   [回到表目錄](#main-table)

### football_leagues

| Column Name      | Data Type           | Default | Attributes  | Comment                |info|
| ---------------- | ------------------- | ------- | ----------- | ---------------------- |--------|
| `id`             | int(11)             | —       | PRIMARY KEY | 聯賽 ID                  | |
| `name_en`        | varchar(255)        | NULL    |             | 聯賽名稱（英文）               | |
| `name_en_short`  | varchar(255)        | NULL    |             | 聯賽簡稱（英文）               | |
| `name_chs`       | varchar(255)        | NULL    |             | 聯賽名稱（簡體中文）             | |
| `name_chs_short` | varchar(255)        | NULL    |             | 聯賽簡稱（簡體中文）             | |
| `name_cht`       | varchar(255)        | NULL    |             | 聯賽名稱（繁體中文）             | |
| `name_cht_short` | varchar(255)        | NULL    |             | 聯賽簡稱（繁體中文）             | |
| `type`           | tinyint(4)          | NULL    |             | 聯賽類型 (1: 聯賽, 2: 盃賽)    |聯賽:1079和盃賽:1102 |
| `sum_round`      | int(11)             | NULL    |             | 總輪數                    |null 不明 |
| `curr_round`     | int(11)             | NULL    |             | 當前輪數                   |null 不明 |
| `curr_season`    | varchar(10)         | NULL    |             | 當前賽季                   |null 不明 |
| `color`          | varchar(10)         | NULL    |             | 顏色代碼                   | |
| `league_logo`    | varchar(255)        | NULL    |             | 聯賽 Logo URL            | |
| `league_logo_s3` | varchar(255)        | NULL    |             | 聯賽 Logo 實際存放位置         | |
| `country_id`     | int(11)             | NULL    |             | 國家 ID                  |澳門是-3，香港是-2。 |
| `is_hot`         | tinyint(1) UNSIGNED | 0       |             | 熱門                     |只有8個是熱門，主要為歐洲 |
| `is_locked`      | tinyint(1) UNSIGNED | 0       | NOT NULL    | 是否鎖定資料 (1: 鎖定, 0: 未鎖定) |未鎖定8個, 鎖定2173個 |
| `level`          | tinyint(1) UNSIGNED | NULL    |             | 聯賽等級                   | 1-4 level, null 有1730個|

```sql
SELECT DISTINCT country_id , name_cht
FROM sports_data.football_leagues
WHERE country_id < 0;
```

- 澳門是-3，香港是-2。

<details>
  <summary><font color=red>表格(點擊後展開)</font></summary>

| `country_id` | 聯賽名稱          |
| ------------ | ------------- |
| -2           | 香港超級聯賽        |
| -2           | 香港足球聯賽盃       |
| -2           | 香港足球總會聯華國際足總盃 |
| -2           | 香港足協主席盃       |
| -2           | 香港足球總會高級銀牌賽   |
| -2           | 香港後備聯賽        |
| -2           | 香港甲組聯賽        |
| -2           | 香港乙組聯賽        |
| -2           | 香港菁英盃         |
| -2           | 香港女子足球超級聯賽    |
| -2           | 香港足球錦標賽       |
| -2           | 香港丙組聯賽        |
| -2           | 香港乙組聯賽盃       |
| -2           | 香港女子盃賽        |
| -2           | 香港丙組聯賽盃       |
| -2           | 香港超級聯賽盃       |
| -2           | 香港足球U22聯賽     |
| -3           | 澳門甲組聯賽        |
| -3           | 澳門乙組聯賽        |
| -3           | 澳門足球會足總盃      |
| -3           | 澳門丙組聯賽        |
</details>
<br>

```sql
SELECT SUM(is_hot) AS total_hot_leagues
FROM sports_data.football_leagues;

SELECT name_cht, is_hot
FROM sports_data.football_leagues
WHERE is_hot = 1;
```

- 只有8個聯賽是熱門的: 西班牙甲組聯賽、英格蘭超級聯賽、法國甲組聯賽、歐洲聯賽歐霸盃、歐洲聯賽冠軍盃、歐洲協會聯賽、意大利甲組聯賽和德國甲組聯賽 

```sql
# 總輪數, 當前輪數, 當前賽季有空值
SELECT DISTINCT *
FROM sports_data.football_leagues
WHERE sum_round IS NULL OR curr_round IS NULL or curr_season IS NULL;

# 聯賽等級1-4 也有空值情況
SELECT DISTINCT `level`
FROM sports_data.football_leagues;

SELECT `level` , name_cht
FROM sports_data.football_leagues
WHERE level IS NULL;

SELECT COUNT(*) AS null_level_count
FROM sports_data.football_leagues
WHERE level IS NULL;

# 未鎖定8個, 鎖定2173個
SELECT is_locked, COUNT(*) AS count
FROM sports_data.football_leagues
GROUP BY is_locked;
```
$\blue\bigstar$   [回到表目錄](#main-table)

### football_lineups

| Column Name   | Data Type     | Default | Attributes            | Comment           |info|
| ------------- | ------------- | ------- | --------------------- | ----------------- |------|
| `match_id`    | `int(11)`     | –       | NOT NULL, PRIMARY KEY | 比賽 ID（主鍵）         ||
| `home_array`  | `varchar(11)` | `NULL`  | –                     | 主隊陣式，例如：442、433 等 |29種，少了424跟2323的戰術|
| `away_array`  | `varchar(11)` | `NULL`  | –                     | 客隊陣式              |31種|
| `home_lineup` | `text`        | `NULL`  | –                     | 主隊首發球員名單列表        |11名，複合屬性:`PlayerID`,`NameChs`,`NameCht`,`Number`,`PositionID`|
| `away_lineup` | `text`        | `NULL`  | –                     | 客隊首發球員名單列表        |11名|
| `home_backup` | `text`        | `NULL`  | –                     | 主隊替補球員名單列表        |候補12名，複合屬性:`PlayerID`,`NameChs`,`NameCht`,`Number`,`PositionID`|
| `away_backup` | `text`        | `NULL`  | –                     | 客隊替補球員名單列表        |候補12名|

```sql
SELECT home_array, COUNT(*) AS count
FROM sports_data.football_lineups
GROUP BY home_array;

SELECT distinct home_array
FROM sports_data.football_lineups;

SELECT COUNT(DISTINCT home_array) AS num_home_array_types
FROM sports_data.football_lineups;

SELECT COUNT(DISTINCT away_array) AS num_away_array_types
FROM sports_data.football_lineups;

# 差集
-- home_array 差 away_array
SELECT DISTINCT home_array AS formation
FROM sports_data.football_lineups
WHERE home_array IS NOT NULL

EXCEPT

SELECT DISTINCT away_array
FROM sports_data.football_lineups
WHERE away_array IS NOT NULL

UNION

-- away_array 差 home_array
SELECT DISTINCT away_array AS formation
FROM sports_data.football_lineups
WHERE away_array IS NOT NULL

EXCEPT

SELECT DISTINCT home_array
FROM sports_data.football_lineups
WHERE home_array IS NOT NULL;
```
$\blue\bigstar$   [回到表目錄](#main-table)

### football_players

| Column Name   | Data Type     | Default | Attributes            |Comment|info|
| ----------------- | ------------ | ---- | ------------ | ----------------------------------- | -------|
| `id`              | int(11)      | –    | NOT NULL, PK | 球員ID                                |總球員265587|
| `name_en`         | varchar(255) | NULL |              | 球員名 - 英文                            ||
| `name_chs`        | varchar(255) | NULL |              | 球員名 - 簡體                            ||
| `name_cht`        | varchar(255) | NULL |              | 球員名 - 繁體                            ||
| `birthday`        | varchar(50)  | NULL |              | 出生日期                                |推算年齡|
| `height`          | varchar(50)  | NULL |              | 身高                                  ||
| `weight`          | varchar(50)  | NULL |              | 體重                                  ||
| `nationality_id`  | int(11)      | NULL |              | 國籍 ID                               |20513為空值,214的國家|
| `photo`           | varchar(255) | NULL |              | 照片 URL（建議添加參數 `?win007=sell`，勿直接調用） ||
| `photo_s3`        | varchar(255) | NULL |              | 照片實際存放位置                            ||
| `value`           | varchar(50)  | NULL |              | 身價（單位：萬歐元）                          ||
| `feet_en`         | varchar(50)  | NULL |              | 慣用腳 - 英文                            |Right, Left, Both, 空值(192220個)|
| `feet_chs`        | varchar(50)  | NULL |              | 慣用腳 - 簡體                            ||
| `feet_cht`        | varchar(50)  | NULL |              | 慣用腳 - 繁體                            ||
| `nationality2_id` | int(11)      | NULL |              | 國籍2 ID                              |192個國家，有雙重國籍? 卻沒有主要國籍37071個|

```sql
-- 總筆數
SELECT COUNT(*) AS total_rows
FROM sports_data.football_players;

-- 國籍(空值無法辨別)
SELECT nationality_id, COUNT(*) AS count
FROM sports_data.football_players
GROUP BY nationality_id;

SELECT COUNT(distinct nationality_id) AS count
FROM sports_data.football_players;

-- 慣用腳
SELECT distinct feet_en
FROM sports_data.football_players
WHERE nationality_id IS NULL;

SELECT feet_en, count(*) as count
FROM sports_data.football_players
WHERE feet_en IS NULL;

-- 身價
SELECT
  COUNT(*) AS total_count,
  COUNT(value) AS non_null_count,
  COUNT(*) - COUNT(value) AS null_count,
  MIN(CAST(value AS DECIMAL(10,2))) AS min_value,
  MAX(CAST(value AS DECIMAL(10,2))) AS max_value,
  AVG(CAST(value AS DECIMAL(10,2))) AS avg_value
FROM sports_data.football_players
WHERE value REGEXP '^[0-9]+(\\.[0-9]+)?$' OR value IS NULL;

-- 其一沒有國籍
SELECT COUNT(*) AS count
FROM sports_data.football_players
WHERE nationality_id is NULL OR nationality2_id is NOT NULL;

SELECT *
FROM sports_data.football_players
WHERE nationality_id is NULL OR nationality2_id is NOT NULL;

-- 沒有主要國籍卻有第二國籍
SELECT count(distinct nationality2_id) as weiredNationstatus
FROM sports_data.football_players
WHERE nationality_id is NULL OR nationality2_id is NOT NULL;
```

- 身價部分（單位：萬歐元）

|total_count| non_null_count| null_count| min_value| max_value|avg_value|
|------|------|------|------|------|------|
|265587	|83145|	182442|	0.40|	20000.00|	79.232251|

$\blue\bigstar$   [回到表目錄](#main-table)

### football_team_players

| Column Name    | Data Type    | Default | Attributes            | Comment                                        |info|
| ------------------- | ------------- | ---- | -------- | ------- |------- |
| `team_id`           | `int(11)`     | 無    | NOT NULL | 所在球隊ID  ||
| `player_id`         | `int(11)`     | 無    | NOT NULL | 球員ID    |
| `position_en`       | `varchar(50)` | NULL |          | 場上位置-英文 |20種，猜測74404空值可能為候補選手|
| `position_chs`      | `varchar(50)` | NULL |          | 場上位置-簡體 ||
| `position_cht`      | `varchar(50)` | NULL |          | 場上位置-繁體 ||
| `number`            | `varchar(10)` | NULL |          | 球衣號碼    |
| `end_date_contract` | `varchar(11)` | NULL |          | 合同到期時間  ||

```sql
SELECT count(distinct position_en) as count
FROM sports_data.football_team_players;

SELECT count(*) as nullcount
FROM sports_data.football_team_players
WHERE position_en is null;
```

$\blue\bigstar$   [回到表目錄](#main-table)

### football_teams

| Column Name    | Data Type    | Default | Attributes            | Comment                                        |info|
| --------------- | ------------------- | ---- | -------- | ----------------------------------- | -------- | 
| `id`            | int(11)             |     | NOT NULL | 球隊 ID（主鍵）                           ||
| `league_id`     | int(11)             |     | NOT NULL | 所屬聯賽 ID                             ||
| `name_en`       | varchar(255)        |     | NOT NULL | 球隊名稱 - 英文                           ||
| `name_chs`      | varchar(255)        |    | NOT NULL | 球隊名稱 - 簡體                           ||
| `name_cht`      | varchar(255)        |     | NOT NULL | 球隊名稱 - 繁體                           ||
| `founding_date` | varchar(10)         | NULL |          | 球隊成立日期（格式：YYYY-MM-DD）               ||
| `area_en`       | varchar(255)        | NULL |          | 所在地 - 英文                            ||
| `area_chs`      | varchar(255)        | NULL |          | 所在地 - 簡體                            ||
| `area_cht`      | varchar(255)        | NULL |          | 所在地 - 繁體                            ||
| `gym_en`        | varchar(255)        | NULL |          | 球場名稱 - 英文                           ||
| `gym_chs`       | varchar(255)        | NULL |          | 球場名稱 - 簡體                           ||
| `gym_cht`       | varchar(255)        | NULL |          | 球場名稱 - 繁體                           ||
| `capacity`      | int(11)             | NULL |          | 球場容量                                ||
| `logo`          | varchar(255)        | NULL |          | 球隊 Logo 圖片 URL（建議加上 `?win007=sell`） ||
| `logo_s3`       | varchar(255)        | NULL |          | 球隊 Logo 實際存放位置                      ||
| `addr_en`       | varchar(255)        | NULL |          | 球隊地址 - 英文                           ||
| `addr_chs`      | varchar(255)        | NULL |          | 球隊地址 - 簡體                           |
| `addr_cht`      | varchar(255)        | NULL |          | 球隊地址 - 繁體                           ||
| `website`       | varchar(255)        | NULL |          | 球隊官方網站                              ||
| `coach_id`      | int(11)             | NULL |          | 主教練 ID                              ||
| `is_national`   | tinyint(1)          | NULL |          | 是否為國家隊（1 是，0 否）                     |空值16, 否47519, 有1354|
| `is_locked`     | tinyint(1) unsigned | 1    | NOT NULL | 名稱是否鎖定（1 鎖定，0 可更新）                  |無參考價值都是1|

```sql
SELECT count(distinct is_national) as count
FROM sports_data.football_team_players;

SELECT is_national, COUNT(*) AS count
FROM sports_data.football_teams
GROUP BY is_national;

SELECT *
FROM sports_data.football_teams
WHERE is_national is null;

SELECT is_locked, COUNT(*) AS count
FROM sports_data.football_teams
GROUP BY is_locked;
```
- 似乎可以手動排除(16筆 人工查證)
![alt text](附檔/image.png)

$\blue\bigstar$   [回到表目錄](#main-table)

### football_technics

| Column Name    | Data Type    | Default | Attributes            | Comment|info|
| --------------- | ------- | --- | -------- | ---------------------------------------------------- |----- |
| `match_id`      | int(11) | 無   | NOT NULL | 比賽 ID（主鍵）                                            |  |
| `technic_count` | text    | 無   | NOT NULL | 技術統計內容。格式為：`技術類型,主隊數值,客隊數值;...` | 34,4,10;37,2,2;14,32%,68%;46,30%,70%;44,35,60; |

> note:  '技術統計內容：以“;”分隔每組數據 “,”分隔每個字段【技術統計類型,主隊技術統計,客隊技術統計】以分號分隔，三項一組，分別為：類型(從0開始編號)，主隊技術統計，客隊技術統計；例：「3,15,4」表示的是「射門次數，主隊15次，客隊4次"；"0,*,"表示的是」先開球，主隊先開球"',

$\blue\bigstar$   [回到表目錄](#main-table)

### football_matches

| Column Name    | Data Type    | Default | Attributes Comment         |info|
| ------------------ | ------------ | ---- | -------------------------- | ---- |
| `id`               | int(11)      | 無    | 比賽 ID（主鍵）                  |      |
| `league_id`        | int(11)      | NULL | 聯賽 ID                      |      |
| `sub_league_id`    | int(11)      | NULL | 子聯賽 ID                     |      |
| `match_time`       | datetime     | NULL | 比賽時間：'yyyy/MM/dd HH:mm:ss' |      |
| `start_time`       | datetime     | NULL | 開場時間。比賽進行時間=當前時間-開場時間（下半場+45分鐘）。state=1：返回上半場開場時間；state=3：返回下半場開場時間。格式：yyyy/MM/dd HH:mm:ss 其它狀態沒有開場時間。    |      |
| `home_id`          | int(11)      | NULL | 主隊 ID                      |      |
| `away_id`          | int(11)      | NULL | 客隊 ID                      |      |
| `state`            | int(11)      | NULL | '比賽狀態。0：未開, 1：上半場, 2：中場, 3：下半場, 4：加時, 5：點球, -1：完場, -10：取消, -11：待定, -12：腰斬, -13：中斷, -14：推遲',         |      |
| `home_score`       | int(11)      | NULL | 主隊得分（常規）                   |      |
| `away_score`       | int(11)      | NULL | 客隊得分（常規）                   |      |
| `home_half_score`  | int(11)      | NULL | 主隊上半場得分                    |      |
| `away_half_score`  | int(11)      | NULL | 客隊上半場得分                    |      |
| `home_red`         | int(11)      | NULL | 主隊紅牌                       |      |
| `away_red`         | int(11)      | NULL | 客隊紅牌                       |      |
| `home_yellow`      | int(11)      | NULL | 主隊黃牌                       |      |
| `away_yellow`      | int(11)      | NULL | 客隊黃牌                       |      |
| `home_corner`      | int(11)      | NULL | 主隊角球數                      |      |
| `away_corner`      | int(11)      | NULL | 客隊角球數                      |      |
| `home_half_red`    | int(11)      | NULL | 主隊上半場紅牌數                   |      |
| `away_half_red`    | int(11)      | NULL | 客隊上半場紅牌數                   |      |
| `home_half_yellow` | int(11)      | NULL | 主隊上半場黃牌數                   |      |
| `away_half_yellow` | int(11)      | NULL | 客隊上半場黃牌數                   |      |
| `home_half_corner` | int(11)      | NULL | 主隊上半場角球數                   |      |
| `away_half_corner` | int(11)      | NULL | 客隊上半場角球數                   |      |
| `home_rank_en`     | varchar(50)  | NULL | 主隊排名（英文）                   |      |
| `home_rank_chs`    | varchar(50)  | NULL | 主隊排名（簡體）                   |      |
| `home_rank_cht`    | varchar(50)  | NULL | 主隊排名（繁體）                   |      |
| `away_rank_en`     | varchar(50)  | NULL | 客隊排名（英文）                   |      |
| `away_rank_chs`    | varchar(50)  | NULL | 客隊排名（簡體）                   |      |
| `away_rank_cht`    | varchar(50)  | NULL | 客隊排名（繁體）                   |      |
| `is_neutral`       | tinyint(1)   | 0    | 是否中立場                      |      |
| `has_lineup`       | tinyint(1)   | 0    | 是否有陣容資料                    |      |
| `has_statistics`   | tinyint(1)   | 0    | 是否有技術統計資料 1：有, 0：無                 |      |
| `group_id`         | int(11)      | NULL |  '盃賽階段ID。與【接口18.杯賽階段類型】groupId匹配；聯賽不返回該字段；部分杯賽無該數據，返回null。'           |      |
| `season`           | varchar(50)  | NULL | 賽季                         |      |
| `round_en`         | varchar(50)  | NULL | 輪次（英文）                     |      |
| `round_chs`        | varchar(50)  | NULL | 輪次（簡體）                     |      |
| `round_cht`        | varchar(50)  | NULL | 輪次（繁體）                     |      |
| `grouping`         | varchar(50)  | NULL | 分組                         |      |
| `location_en`      | varchar(100) | NULL | 場地（英文）                     |      |
| `location_chs`     | varchar(100) | NULL | 場地（簡體）                     |      |
| `location_cht`     | varchar(100) | NULL | 場地（繁體）                     |      |
| `weather_en`       | varchar(100) | NULL | 天氣（英文）                     |      |
| `weather_chs`      | varchar(100) | NULL | 天氣（簡體）                     |      |
| `weather_cht`      | varchar(100) | NULL | 天氣（繁體）                     |      |
| `temp`             | varchar(10)  | NULL | 溫度                         |      |
| `extra_explain`    | varchar(50)  | NULL | 比賽說明2。數據分為2部分，用“｜”分隔。例如：2;｜90,1-0;2-2;1,1-0;2-4;2                  | |
| `is_hidden`        | tinyint(1)   | 0    | ???                      |      |
| `injury_time`      | tinyint(4)   | NULL | 上下半場補時計長。上下半場補時的時長，補時進行到多少分鐘需客戶自行計算。上半場超過45分鐘開始，下半場超過90分鐘開始。                       |  都是0    |
| `var`              | varchar(255) | NULL | VAR 事件                     |      |
| `update_time`      | datetime     | NULL | 數據更新時間                     |      |
| `ishkjc`           | tinyint(1)   | 0    | 自定義欄位（未具體說明）               |  是否為香港馬會賽事。ishkjc = true 代表"香港馬會賽事"(精選賽事)    |
| `deleted`          | tinyint(1)   | 0    | 是否刪除賽程（1: 刪除）              |      |

$\blue\bigstar$   [回到表目錄](#main-table)

### football_events

| Column Name    | Data Type    | Default | Attributes Comment         |info|
| ---------- | ------- | ---- | --------- |--------- |
| `match_id` | int(11) | 否    | 比賽 ID（主鍵） | |
| `event`    | text    | 否    | 事件列表      | 複合屬性:`Id`,`IsHome`,`Kind`,`Time`,`NameEn`,`NameChs`,`NameCht`,`PlayerId1`,`PlayerId2`,`Overtime`|

<details>
  <summary><font color=red>event (點擊後展開)</font></summary>

> |column|data type|info|
> | ----- | ----- | ----- |
> |Id|int||
> |IsHome|boolean|true: 主隊事件<br> false:客隊事件|
> |Kind|int|1：入球<br> 2：紅牌<br> 3：黃牌<br> 7：點球<br> 8：烏龍<br> 9：兩黃變紅<br> 11：換人<br> 13：射失點球<br> 14：視頻裁判（VR裁判）|
> |Time|string|時間:第n分鐘|
> |NameEn|string|球員姓名-英文-含助攻球員|
> |NameChs|string|球員姓名-簡體-含助攻球員|
> |NameCht|string|球員姓名-繁體-含助攻球員|
> |PlayerId1|string|球員ID|
> |PlayerId2|string|球員ID下場球員或助攻球員|
> |Overtime|string|傷停補時時間|
</details>
<br>

$\blue\bigstar$   [回到表目錄](#main-table)

## other 補充
- [我們自己的-lmgoal](https://m.lmgoal.com/)
<br>
- 比較指標性的比分網
    - [雷速體育-連結](https://www.leisu.com/)
    - [Sofascore-連結](https://www.sofascore.com/zh/)
    - [AIScore-連結](https://www.aiscore.com/zht)
- 運彩網
    - [連結 要proxy](https://hga050.com/)
    - [bet365-連結](https://www.bet365.de/)

<br>

- 聯賽（League）

| 項目         | 說明                                                    |
| ---------- | ----------------------------------------------------- |
| **制度**     | 採 **積分制循環賽**，每隊對戰多次（通常主客場各一次）。                        |
| **排名依據**   | 根據每場比賽的 **勝/平/負** 所得分數累積（勝=3分，平=1分，負=0分）。最終依總積分決定排名。  |
| **比賽場次**   | 每隊比賽場數固定，通常較多。舉例：英超有20隊，每隊打38場（19隊 × 2）。              |
| **持續時間**   | 賽季長，通常為 **半年至一年**（例：2024/08 \~ 2025/05）。              |
| **冠軍決定方式** | 賽季結束後，積分最高者為冠軍（若積分相同，看淨勝球等）。                          |
| **例子**     | 英格蘭超級聯賽（Premier League）、西班牙甲級聯賽（La Liga）、中華民國企業甲級聯賽等。 |

- 盃賽（Cup）

| 項目         | 說明                                                       |
| ---------- | -------------------------------------------------------- |
| **制度**     | 採 **淘汰賽制度**（或混合賽制，初期分組+淘汰賽），輸一場即被淘汰（部分可能打主客兩回合）。         |
| **排名依據**   | 每場比賽的勝負決定是否晉級下一輪；沒有積分制度。                                 |
| **比賽場次**   | 比賽場數不固定，取決於隊伍晉級情況；整體比賽場次比聯賽少。                            |
| **持續時間**   | 持續時間較短，可為幾週至幾個月不等。                                       |
| **冠軍決定方式** | 通常為 **單場決賽**（或主客兩回合），勝者奪冠。                               |
| **例子**     | 英格蘭足總盃（FA Cup）、歐洲國家盃（Euro）、世界盃（FIFA World Cup）、中華民國總統盃等。 |

| 特點  | 聯賽          | 盃賽              |
| --- | ----------- | --------------- |
| 穩定性 | 積分制度，長期表現為主 | 淘汰賽，爆冷可能性高      |
| 公平性 | 所有球隊都互相對戰   | 抽籤安排對戰，可能運氣影響結果 |
| 強調  | 一致性、耐力      | 臨場發揮、決戰能力       |
