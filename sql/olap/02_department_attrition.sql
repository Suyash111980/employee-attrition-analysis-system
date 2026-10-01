SELECT
    d.DepartmentName,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimDepartment d
    ON f.DepartmentKey = d.DepartmentKey
GROUP BY d.DepartmentName
ORDER BY AttritionRate DESC;