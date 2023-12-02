
### Общее описание решений
1. Сделал git clone своего репозитория
2. Открыл папку geometric_lib через терминал
2. Создал ветку documentation_(мой ису)
3. Описал решение файлов rectangle.py и triangle.py в VS
4. Сделал git add и git commit каждому файлу
5. Установил расширение Markdown в VS
---
# Math formulas
## Area
- Circle: S = πR²
- Rectangle: S = ab
- Square: S = a²
## Perimeter
- Circle: P = 2πR
- Rectangle: P = 2a + 2b
- Square: P = 4a

___
### Описание каждой функции с примерами вызова

* __Circle:__
_def area(r):_
   _return math.pi * r * r_
``` 
in: 5
out: 78,5
```

* __Rectangle:__
_def rectangle(a, b):
   return a * b_
``` 
in: 5 6
out: 30
```

* __Square:__
_def square(a):
   return a * a_
``` 
in: 5
out: 25
```

* __Circle:__
_def circle(r):
return meth.pi * r * 2_
``` 
in: 5
out: 31,4
```

* __Rectangle:__
_def rectangle(a, b):
return 2 * a + 2 * b_
``` 
in: 5 6
out: 22
```

* __Square:__
_def square(a):
return 4 * a_

``` 
in: 5
out: 20
```

___
### ___Rectangle.py___

```
Функция нахождения площади прямоугольника.
```
**def area(a, b):** 
    *'''Принимает число a и число b, возвращает их умножение, возвращает площадь'''* 
    **return a * b**
 >> __Пример__: 
 _Ввод_: 5 2
 _Вывод_: 10

```
Функция нахождения периметра прямоугольника.
```
 **def perimeter(a, b):** 
    *'''Принимает число a и число b, возвращает умноженную на два их сумму, возвращает периметр'''*
    **return (a + b) * 2**
 >> __Пример__: 
 _Ввод_: 5 2
 _Вывод_: 14

 
 
 ### ___Triangle.py___
 
```
Функция нахождения площади треугольника.
```
**def area(a, h):**
    *'''Принимает a, h, возвращает площадь треугольника, a умноженную на половину h'''*
    **return a * h / 2**
 >> __Пример__: 
 _Ввод_: 10 8
 _Вывод_: 40
 
 ```
 Функция нахождения периметра треугольника.
 ```
 **def perimeter(a, b, c):** 
    *'''Принимает a, b, c, возвращает периметр треугольника, сумму всех чисел'''*
    **return a + b + c**
 >> __Пример__: 
 _Ввод_: 1 2 3 
 _Вывод_: 6
 ---

 ## _История изменения проекта с хешами комитов (кроме последней записи)_

 commit **888d8e087af948808893844927d4334913da8efc**
Author: Chernykh <chernykharseniy18@mail.ru>
Date:   Thu Sep 13 12:50:51 2023 +0300

    new file

commit **2f3c72bf4060c383f33e4903da2e6c656ca904bc** (origin/new_features_409838)
Author: Chernykh <chernykharseniy18@mail.ru>
Date:   Thu Sep 13 12:56:47 2023 +0300

    new file 2

commit **1a49f62ec6fce3197e35f3ed68b6978df1ff99c4** (origin/main, origin/HEAD, main)
Author: Chernykh <chernykharseniy18@mail.ru>
Date:   Thu Sep 13 13:00:06 2023 +0300

    error fixed

commit **9b4ff6ebbc1ff61cb2606fbb6557602483726496**
Author: Chernykh <chernykharseniy18@mail.ru>
Date:   Thu Sep 28 15:05:42 2023 +0300

    docs rectangle.py







