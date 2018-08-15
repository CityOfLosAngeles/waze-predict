
Select distinct(street), avg(regular_speed), avg(speed), avg(regular_speed) - avg(speed) as Avg_Diff_Speed
from waze2.irregularities
group by street
Order By Avg_Diff_Speed desc


Select distinct(street), count(street)
From waze2.jams
Group by street
Order by count(street) desc;


Select street, avg(speed)
From waze2.jams
Group by street
Order by avg(speed) desc;


Select distinct(road_type), count(road_type)
From waze2.jams
Group by road_type
Order by count(road_type);




Select distinct(street), avg(delay)
From waze2.jams
Group by street
Order by avg(delay) desc;


Select distinct(street), type, count(type)
From waze2.alerts
Group by street, type
Order by count(type) desc;


Select distinct(street), avg(delay_seconds)
From waze2.irregularities 
Group by street
Order by avg(delay_seconds) desc;


Select distinct street, avg(length)
From waze2.jams
Group by street
Order by avg(length) desc;


Select distinct(street), avg(length)
from waze2.irregularities
group by street
order by avg(length) desc;


Select distinct(street), sum(alerts_count)
from waze2.irregularities 
group by street
Order by sum(alerts_count) desc;

Select detection_date
From waze2.irregularities
where detection_date like '%Feb%

Select  type, count(type)
From waze2.alerts
Group by type
Order by count(type) desc;

Select distinct(street), type, count(type)
From waze2.alerts
where type like 'JAM'
Group by street, type
Order by count(type) desc;
