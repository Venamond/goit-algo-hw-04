# Порівняння алгоритмів сортування

| case     | n     | algorithm      | time_s_median |
|----------|-------|----------------|---------------|
| random   | 1000  | Insertion      | 0.013204      |
| random   | 1000  | Merge          | 0.001125      |
| random   | 1000  | Timsort sort   | 0.000002      |
| random   | 1000  | Timsort sorted | 0.000044      |
| random   | 5000  | Insertion      | 0.344390      |
| random   | 5000  | Merge          | 0.006670      |
| random   | 5000  | Timsort sort   | 0.000015      |
| random   | 5000  | Timsort sorted | 0.000356      |
| random   | 10000 | Insertion      | 1.418977      |
| random   | 10000 | Merge          | 0.014294      |
| random   | 10000 | Timsort sort   | 0.000029      |
| random   | 10000 | Timsort sorted | 0.000871      |
| random   | 20000 | Merge          | 0.030424      |
| random   | 20000 | Timsort sort   | 0.000061      |
| random   | 20000 | Timsort sorted | 0.001939      |
| reversed | 1000  | Insertion      | 0.026035      |
| reversed | 1000  | Merge          | 0.000773      |
| reversed | 1000  | Timsort sort   | 0.000002      |
| reversed | 1000  | Timsort sorted | 0.000004      |
| reversed | 5000  | Insertion      | 0.703451      |
| reversed | 5000  | Merge          | 0.004601      |
| reversed | 5000  | Timsort sort   | 0.000012      |
| reversed | 5000  | Timsort sorted | 0.000026      |
| reversed | 10000 | Insertion      | 2.850762      |
| reversed | 10000 | Merge          | 0.009689      |
| reversed | 10000 | Timsort sort   | 0.000022      |
| reversed | 10000 | Timsort sorted | 0.000042      |
| reversed | 20000 | Merge          | 0.020211      |
| reversed | 20000 | Timsort sort   | 0.000043      |
| reversed | 20000 | Timsort sorted | 0.000082      |
| sorted   | 1000  | Insertion      | 0.000074      |
| sorted   | 1000  | Merge          | 0.000766      |
| sorted   | 1000  | Timsort sort   | 0.000002      |
| sorted   | 1000  | Timsort sorted | 0.000003      |
| sorted   | 5000  | Insertion      | 0.000385      |
| sorted   | 5000  | Merge          | 0.004369      |
| sorted   | 5000  | Timsort sort   | 0.000012      |
| sorted   | 5000  | Timsort sorted | 0.000024      |
| sorted   | 10000 | Insertion      | 0.000778      |
| sorted   | 10000 | Merge          | 0.009256      |
| sorted   | 10000 | Timsort sort   | 0.000022      |
| sorted   | 10000 | Timsort sorted | 0.000037      |
| sorted   | 20000 | Merge          | 0.019276      |
| sorted   | 20000 | Timsort sort   | 0.000044      |
| sorted   | 20000 | Timsort sorted | 0.000100      |

---

## Висновки

1. **Insertion sort**  
   - Має квадратичну складність `O(n²)` і на малих вибірках (n=1000) ще може показувати прийнятний час.  
   - Але вже при n=5000–10000 час роботи стає дуже великим (секунди), що підтверджує непридатність цього алгоритму для великих обсягів даних.

2. **Merge sort**  
   - Працює стабільно з оцінкою `O(n log n)`.  
   - Швидший за Insertion на великих n, але завжди повільніший за Timsort.  
   - Для масивів 20 000 елементів час ~0.02–0.03 секунд, що досить ефективно, проте вдвічі–втричі гірше за Timsort.

3. **Timsort (list.sort / sorted)**  
   - Є найефективнішим: на всіх наборах даних (`random`, `reversed`, `sorted`) стабільно працює в тисячі разів швидше за Insertion і в десятки разів швидше за Merge.  
   - Вбудований `list.sort()` трохи швидший за `sorted()`, оскільки сортує «на місці» і не створює копію.  
   - Адаптивність Timsort дозволяє ефективно працювати і з уже відсортованими масивами (час практично не зростає).

---

### Загальний висновок
- Для навчальних цілей алгоритми Insertion та Merge корисні, оскільки добре ілюструють базові підходи.  
- Проте для практичного використання варто застосовувати **вбудований Timsort у Python (`list.sort()` або `sorted()`)**, який поєднує сильні сторони сортування вставками та злиттям, є адаптивним та значно ефективнішим.  