select sum(l.amount) as totalloan_amounts, sum(l.total_payment) as totalloan_payments from loans l inner join
contribution_month cm on month(str_to_date(concat(cm.month,' ',cm.year),'%M %d %Y')) = month(l.date_rel)
where year(l.date_rel) = 2014 and month(l.date_rel) = 1