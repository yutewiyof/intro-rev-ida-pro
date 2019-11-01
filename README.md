# Initial page

Бэкап перевода Яши с wasm.in цикла статей "Введение в реверсинг с нуля, используя IDA PRO" от Рикардо Нарвахи

[**Gitbook версия**](https://yutewiyof.gitbook.io/intro-rev-ida-pro/)

## Сборка

Необходимо установить pandoc [https://pandoc.org/](https://pandoc.org/)

### Epub

В папке с файлами *.md необходимо выполнить команду

```cmd
pandoc -f markdown -t epub -o ida.epub README.md chast-01.md chast-02.md chast-03.md chast-04.md chast-05.md chast-06.md chast-07.md chast-08.md chast-09.md chast-10.md chast-11.md chast-12.md chast-13.md chast-14.md chast-15.md chast-16.md chast-17.md chast-18.md chast-19.md chast-20.md chast-21.md chast-22.md chast-23.md chast-24.md chast-25.md chast-26.md chast-27.md chast-28.md chast-29.md chast-30.md chast-31.md chast-32.md chast-33.md chast-34.md chast-35.md chast-36.md chast-37.md chast-38.md chast-39.md chast-40.md chast-41.md chast-42.md chast-43.md chast-44.md chast-45.md chast-46.md chast-47.md chast-48.md chast-49.md chast-50.md chast-51.md chast-52.md chast-53.md chast-54.md chast-55.md chast-56.md chast-57.md chast-58.md chast-59.md chast-60.md chast-61.md chast-62.md chast-63.md chast-64.md chast-65.md chast-66.md chast-67.md
```

### FB2

```cmd
pandoc -f markdown -t fb2 -o ida.fb2 README.md chast-01.md chast-02.md chast-03.md chast-04.md chast-05.md chast-06.md chast-07.md chast-08.md chast-09.md chast-10.md chast-11.md chast-12.md chast-13.md chast-14.md chast-15.md chast-16.md chast-17.md chast-18.md chast-19.md chast-20.md chast-21.md chast-22.md chast-23.md chast-24.md chast-25.md chast-26.md chast-27.md chast-28.md chast-29.md chast-30.md chast-31.md chast-32.md chast-33.md chast-34.md chast-35.md chast-36.md chast-37.md chast-38.md chast-39.md chast-40.md chast-41.md chast-42.md chast-43.md chast-44.md chast-45.md chast-46.md chast-47.md chast-48.md chast-49.md chast-50.md chast-51.md chast-52.md chast-53.md chast-54.md chast-55.md chast-56.md chast-57.md chast-58.md chast-59.md chast-60.md chast-61.md chast-62.md chast-63.md chast-64.md chast-65.md chast-66.md chast-67.md
```

## TODO:

1. поправить глупые смысловые ошибки
2. ~~выполнить разбиение на блоки, перенести иллюстрации на гит~~
3. ~~разбить части на подглавы, дополнить описания частей, поправить оформление, примеры кода~~
4. переписать в виде обычных таблиц картинки с таблицами, и прочие скриншоты из книг
5. перенести бинарные файлы на которых показываются примеры (а надо ли?)
6. недостает 66 часть 2 (ждать перевод Яши / либо перевести)
7. состряпать инструкцию по конвертации \*.md to \*.tex и сборке PDF/EPUB/FB2
8. ~~Исправить скриншот .gitbook/assets/12/47.png, для сравнения смотри на .gitbook/assets/12/45.png~~
9. В главах 26, 64 выделить включевые слова по аналогии с прочими главами.
10. Требуется глобальная вычитка на предмет приведения всех слов и терминов к единообразному стилю / именованию, все числовые значения. строки кода оформить соответствующим тегом \(\'\*стркоа\*\'\), вместо выделения жирным
11. Требуется переформулировать предложени с формулировками "Мы" и сократить повествовательную форму. Все должно быть в повелевающем наклонении.

[ricardonarvaja.info](http://ricardonarvaja.info)

[Введение в реверсинг с нуля, используя IDA PRO - на английском (PDF)](http://ricardonarvaja.info/WEB/INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO/EN%20INGLES/)

[Введение в реверсинг с нуля, используя IDA PRO - на испанском (Word)](http://ricardonarvaja.info/WEB/INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO/)
