select *
  from countries_of_the_world cw
  /*left*/ join country_name cn on cn."name" = trim(cw.coutry)
  /*left*/ join worldcitiespop w on lower(w.country) = lower(cn.country) 
 where cw.coutry = 'Kazakhstan '
   and w.city like 'alma%'
  
select count(c.country) cnt, c.continent 
  from continent c 
 group by c.continent 
 order by cnt
 
 
select *
  from country_name cn 
 where cn."name" like 'Antigua%'
 
select *
  from worldcitiespop w 