SELECT
    AttritionFlag,
    COUNT(*) AS EmployeeCount,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM FactEmployeeAttrition),
        2
    ) AS Percentage
FROM FactEmployeeAttrition
GROUP BY AttritionFlag
ORDER BY AttritionFlag;