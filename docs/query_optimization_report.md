# SQL Query Optimization Report

## Project

SupportPulse

---

# Task 1 - Remove SELECT *

### Original

Used

```sql
SELECT *
```

### Optimized

Selected only required columns.

### Benefits

- Reduced unnecessary columns
- Improved readability
- Reduced memory usage
- Better maintainability

---

# Task 2 - Filter Before JOIN

### Original

Joined complete datasets before filtering.

### Optimized

Filtered customers before joining.

### Benefits

- Smaller intermediate dataset
- Faster joins
- Lower memory usage

---

# Task 3 - Replace Nested Query with CTE

### Original

Used nested subqueries.

### Optimized

Used Common Table Expression (CTE).

### Benefits

- Easier to understand
- Easier to debug
- Better modularity
- Improved maintainability

---

# Best Practices Applied

- Avoided `SELECT *`
- Used explicit column selection
- Applied filters before JOIN
- Used CTE for readability
- Used meaningful aliases

---

# Performance Improvements

| Task | Improvement |
|-------|-------------|
| Remove SELECT * | Reduced selected columns |
| Filter Before JOIN | Reduced rows before joining |
| CTE | Improved readability |

---

# Conclusion

The optimized queries follow SQL best practices by reducing unnecessary data retrieval, minimizing intermediate join sizes, and improving query readability through CTEs. These techniques help analytical queries scale efficiently as datasets grow.