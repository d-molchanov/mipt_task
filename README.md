# Программа для загрузки изображения в виде “сырых” данных и отображения его на экране

## Описание

Изображение в виде “сырых” данных представляет собой csv файл содержащий набор строк, каждая строка состоит из массива целых чисел со значениями в диапазоне от 0 до 255, разделенных символом “;”. Каждое число показывает собой значение пикселя изображения, порядковый номер числа в строке и порядковый номер строки определяют положение пикселя (В csv файле содержится grayscale изображение, поэтому каждый пиксель представлен одним числом). Например, число 24, находящееся в 8-й строке, на 23-м месте означает, что значение пикселя в позиции (7, 22) равно 24 (Положение отчитывается от левого верхнего угла, от нулевого значения).

## Программа реализует следующий функционал:

- выбор csv файла для открытия;
- отображение изображения на экране;
- сохранения открытого файла в файл в виде одного из форматов изображения (jpg, bng, bmp);
- выбор нескольких csv файлов для открытия;
- переключениe между файлами при присмотре в случае открытия нескольких файлов;
- обработка файлов, содержащих данные о цветных изображениях;
- установка цветовой карты на grayscale-изображения;
- показ слайд-шоу выбранных изображений с заданным интервалом; 
- изменение интервала показа изображений.

## Файлы программы

- *main.py*: содержит точку входа для выполняемой программы;
- *image_maker.py*: содержит класс ImageMaker, осуществляющий обработку csv-файлов;
- *main_window.py*: содержит класс MainWindow, осуществляющий логику работы главного окна программы; 
- *child_window.py*: содержит класс ChildWindow, осуществляющий логику работы дочерних окон программы; 
- *main_window_design.py*: содержит дизайн главного окна программы;
- *child_window_design.py*: содержит дизайн дочерних окон программы.