-- 1. Total fact records
SELECT COUNT(*) AS TotalFactRecords
FROM FactEmployeeAttrition;


-- 2. Attrition distribution
SELECT
    AttritionFlag,
    COUNT(*) AS EmployeeCount
FROM FactEmployeeAttrition
GROUP BY AttritionFlag
ORDER BY AttritionFlag;


-- 3. Check invalid AttritionFlag values
SELECT COUNT(*) AS InvalidAttritionFlags
FROM FactEmployeeAttrition
WHERE AttritionFlag NOT IN (0, 1);


-- 4. Check dimension relationships
SELECT COUNT(*) AS InvalidEmployeeKeys
FROM FactEmployeeAttrition f
LEFT JOIN DimEmployee e
    ON f.EmployeeKey = e.EmployeeKey
WHERE e.EmployeeKey IS NULL;


SELECT COUNT(*) AS InvalidJobKeys
FROM FactEmployeeAttrition f
LEFT JOIN DimJob j
    ON f.JobKey = j.JobKey
WHERE j.JobKey IS NULL;


SELECT COUNT(*) AS InvalidDepartmentKeys
FROM FactEmployeeAttrition f
LEFT JOIN DimDepartment d
    ON f.DepartmentKey = d.DepartmentKey
WHERE d.DepartmentKey IS NULL;


SELECT COUNT(*) AS InvalidSatisfactionKeys
FROM FactEmployeeAttrition f
LEFT JOIN DimSatisfaction s
    ON f.SatisfactionKey = s.SatisfactionKey
WHERE s.SatisfactionKey IS NULL;


SELECT COUNT(*) AS InvalidWorkLifeKeys
FROM FactEmployeeAttrition f
LEFT JOIN DimWorkLife w
    ON f.WorkLifeKey = w.WorkLifeKey
WHERE w.WorkLifeKey IS NULL;