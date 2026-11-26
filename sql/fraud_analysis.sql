-- 1. Portfolio KPIs
SELECT COUNT(*) transactions, SUM(amount_cad) volume, SUM(confirmed_fraud) fraud_cases, AVG(confirmed_fraud) fraud_rate FROM transactions;

-- 2. Monthly loss trend
SELECT substr(date,1,7) month, SUM(gross_loss_cad) gross_loss, SUM(net_loss_cad) net_loss FROM transactions GROUP BY 1 ORDER BY 1;

-- 3. Fraud categories
SELECT fraud_category, COUNT(*) cases, SUM(gross_loss_cad) gross_loss FROM transactions WHERE confirmed_fraud=1 GROUP BY 1 ORDER BY 3 DESC;

-- 4. Province exposure
SELECT province, COUNT(*) transactions, SUM(net_loss_cad) net_loss FROM transactions JOIN customers USING(customer_id) GROUP BY 1 ORDER BY 3 DESC;

-- 5. Channel fraud rate
SELECT channel, COUNT(*) transactions, AVG(confirmed_fraud) fraud_rate FROM transactions GROUP BY 1 ORDER BY 3 DESC;

-- 6. Recovery rate
SELECT SUM(recovered_cad) recovered, SUM(recovered_cad)/NULLIF(SUM(gross_loss_cad),0) recovery_rate FROM transactions;

-- 7. Alert performance
SELECT SUM(alert_flag*confirmed_fraud) true_positives, SUM(alert_flag*(1-confirmed_fraud)) false_positives, SUM((1-alert_flag)*confirmed_fraud) false_negatives FROM transactions;

-- 8. Repeated confirmed incidents
SELECT customer_id, COUNT(*) cases, SUM(net_loss_cad) net_loss FROM transactions WHERE confirmed_fraud=1 GROUP BY 1 HAVING COUNT(*)>1 ORDER BY 3 DESC;

-- 9. Monthly fraud rate
SELECT substr(date,1,7) month, AVG(confirmed_fraud) fraud_rate FROM transactions GROUP BY 1 ORDER BY 1;

-- 10. Loss concentration
SELECT transaction_id, fraud_category, net_loss_cad, RANK() OVER(ORDER BY net_loss_cad DESC) loss_rank FROM transactions WHERE confirmed_fraud=1 ORDER BY loss_rank LIMIT 20;