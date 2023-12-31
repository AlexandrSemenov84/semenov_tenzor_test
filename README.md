mini readability
=======================

Тестовое задание Семенова А. В. на позицию разработчика в ООО «Тензор», г. Рыбинск

Программа извлекает данные веб-страницы, указанной в параметре, и сохраняет их в txt-файл.

Описание алгоритма
-----
Подготовка данных:
- Разбираем ответ с помощью библиотеки BeautifulSoup.
- Находим и удаляем из дерева ненужные элементы ('header', 'nav', 'sup', 'footer'), невидимые блоки, а так же списки, состоящие только из тегов 'a'. 
- Обработка таблиц выходит за рамки тестового задания. Все таблицы так же удаляем из дерева.

Извлечение данных:
- Находим теги, которые могу содержать искомые данные ('h1', 'h2', 'h3', 'p', 'ul', 'ol', 'pre')
- Сортируем список найденных тегов по полю sourceline
- Перебираем список. Когда встречаем заголовок, создаем объект Atricle. Все последующие теги - не заголовки конкатенируем в контентное поле объекта. Пока не встретится следующий заголовок.
- На выходе функции получаем список объектов Article

Форматирование:
- Читаем с диска содержимое шаблона template.txt
- Если шаблон валидный, сводим список статей в строку по данному шаблону.

Для точного разбора отдельных ресурсов возможно использовать специализированные экстракторы. Это классы - наследники AbstractExtractor, располагаемые в модуле extractors.py 

To Do
-----

- Доработка функции parse для извлечения данных из элементов div
- Расширить список специализированных экстракторов
- Обработка элементов table
- Расширение атрибутного состава Article

Известные проблемы
--------------

- Неверный url в списке результатов поиска google.com

Результаты тестирования
-----
1. https://ru.wikipedia.org/wiki/Глобальная_блокировка_интерпретатора

```
	Глобальная блокировка интерпретатора

Глобальная блокировка интерпретатора (англ.[/wiki/Английский_язык] Global
Interpreter Lock, GIL) — способ синхронизации потоков[/wiki/Поток_выполнения],
который используется в некоторых
интерпретируемых[/wiki/Интерпретируемый_язык_программирования] языках
программирования[/wiki/Язык_программирования], например в Python[/wiki/Python] и
Ruby[/wiki/Ruby].


	Суть концепции

GIL является самым простым способом избежать конфликтов при одновременном
обращении разных потоков к одним и тем же участкам памяти. Когда один поток
захватывает его, GIL, работая по принципу мьютекса[/wiki/Мьютекс], блокирует
остальные. Нет параллельных потоков — нет конфликтов при обращении к разделяемым
объектам. Очерёдность выполнения потоков определяет
интерпретатор[/wiki/Интерпретатор] в зависимости от реализации, переключение
между потоками может происходить: когда активный поток пытается осуществить
ввод-вывод[/wiki/Ввод-вывод], по исчерпании лимита выполненных
инструкций[/wiki/Код_операции#Программные_наборы_инструкций], либо по таймеру.


	Преимущества и недостатки

Главный недостаток подхода обеспечения потокобезопасности[/wiki/Thread-safety]
при помощи GIL — это ограничение параллельности
вычислений[/wiki/Параллельные_вычисления]. GIL не позволяет достигать наибольшей
эффективности вычислений при работе на
многоядерных[/wiki/Многоядерный_процессор] и
мультипроцессорных[/wiki/Мультипроцессор] системах. Также использование
нескольких потоков накладывает издержки на их переключение из-за эффекта
конкуренции[/wiki/Параллелизм_(информатика)] (потоки «пытаются» перехватить
GIL). То есть многопоточное выполнение может занять большее время, чем
последовательное выполнение тех же задач.

Причины использования GIL:

• Однопоточные сценарии[/wiki/Скрипт] выполняются значительно быстрее, чем при
использовании других подходов обеспечения потокобезопасности;
• Простая интеграция библиотек[/wiki/Библиотека_(программирование)] на
C[/wiki/Си_(язык_программирования)], которые зачастую тоже не потокобезопасны;
• Простота реализации.


	Применение

GIL используется в CPython[/wiki/CPython]'е, наиболее распространённой
реализации интерпретатора языка Python[/wiki/Python], и в Ruby
MRI[/w/index.php?title=Ruby_MRI&action=edit&redlink=1], эталонной реализации
интерпретатора языка Ruby[/wiki/Ruby], где он зовётся Global VM Lock.

В сети[/wiki/Интернет] не раз появлялись петиции[/wiki/Петиция] и открытые
письма[/wiki/Открытое_письмо_(жанр_публичных_выступлений)] с просьбой убрать GIL
из Python'а. Однако создатель и «великодушный пожизненный
диктатор[/wiki/Великодушный_пожизненный_диктатор]» проекта Гвидо ван
Россум[/wiki/Гвидо_ван_Россум] заявляет, что GIL не так уж и плох и он будет в
CPython'е до тех пор, пока кто-то другой не представит реализацию Python'а без
GIL, с которой бы однопоточные скрипты работали так же быстро.

Реализации интерпретаторов на JVM[/wiki/JVM] (Jython[/wiki/Jython],
JRuby[/wiki/JRuby]) и на .NET[/wiki/.NET] (IronPython[/wiki/IronPython],
IronRuby[/wiki/IronRuby]) не используют GIL.

В рамках проекта PyPy[/wiki/PyPy] ведётся работа по реализации транзакционной
памяти[/wiki/Программная_транзакционная_память]
(англ.[/wiki/Английский_язык] Software Transactional Memory, SТМ). На данный
момент даже в многопоточных вычислениях интерпретатор с STM работает во много
раз медленней, чем с GIL. Но за счёт JIT[/wiki/JIT] PyPy-STM всё равно быстрее,
чем CPython.


	Примечания

1. ↑ Thread State and the Global Interpreter
Lock[https://docs.python.org/2/c-api/init.html#threads]. Дата обращения: 21
декабря 2013. Архивировано[https://web.archive.org/web/20131224110750/http://doc
s.python.org/2/c-api/init.html#threads] 24 декабря 2013 года.
2. ↑ Antoine Pitrou. Reworking the GIL[http://mail.python.org/pipermail/python-
dev/2009-October/093321.html]. Python Mailing Lists[http://mail.python.org] (25
октября 2009). Дата обращения: 21 декабря 2013. Архивировано[https://web.archive
.org/web/20110610164607/http://mail.python.org/pipermail/python-
dev/2009-October/093321.html] 10 июня 2011 года.
3. ↑ Описание GIL[https://wiki.python.org/moin/GlobalInterpreterLock]. Python
Wiki[https://wiki.python.org]. Дата обращения: 21 декабря 2013. Архивировано[htt
ps://web.archive.org/web/20131224211753/https://wiki.python.org/moin/GlobalInter
preterLock] 24 декабря 2013 года.
4. ↑ David Beazley. Inside the Python GIL[http://www.dabeaz.com/python/GIL.pdf].
Chicago: Chicago Python User Group[http://chipy.org/] (11 июня 2009). Дата
обращения: 7 октября 2009. Архивировано[https://web.archive.org/web/201012242010
32/http://www.dabeaz.com/python/GIL.pdf] 24 декабря 2010 года.
5. ↑ Shannon -jj Behrens. Concurrency and Python[http://www.ddj.com/linux-open-
source/206103078?pgno=2] 2. Dr. Dobb's Journal[/wiki/Dr._Dobb's_Journal] (3
февраля 2008). Дата обращения: 12 июля 2008. Архивировано[https://web.archive.or
g/web/20080626014054/http://www.ddj.com/linux-open-source/206103078?pgno=2] 26
июня 2008 года.
6. ↑ An open letter to Guido van Rossum: Mr Rossum, tear down that
GIL![https://web.archive.org/web/20131224100921/http://www.snaplogic.com/blogan-
open-letter-to-guido-van-rossum-mr-rossum-tear-down-that-gil/]
SnapLogic[https://en.wikipedia.org/wiki/SnapLogic] (9 сентября 2007).
Архивировано из оригинала[http://www.snaplogic.com/blogan-open-letter-to-guido-
van-rossum-mr-rossum-tear-down-that-gil/] 24 декабря 2013 года.
7. ↑ Guido van Rossum[/wiki/Guido_van_Rossum]. the future of the
GIL[http://mail.python.org/pipermail/python-3000/2007-May/007414.html]. Python
Mailing Lists[http://mail.python.org] (8 мая 2007). Дата обращения: 21 декабря
2013. Архивировано[https://web.archive.org/web/20201109025224/https://mail.pytho
n.org/pipermail/python-3000/2007-May/007414.html] 9 ноября 2020 года.
8. ↑ Guido van Rossum. It isn't Easy to Remove the
GIL[http://www.artima.com/weblogs/viewpost.jsp?thread=214235].
artima.com[http://www.artima.com] (10 сентября 2007). Дата обращения: 21 декабря
2013. Архивировано[https://web.archive.org/web/20190606085140/https://www.artima
.com/weblogs/viewpost.jsp?thread=214235] 6 июня 2019 года.
9. ↑ WhyJython[https://wiki.python.org/jython/WhyJython]. Python Wiki. Дата
обращения: 21 декабря 2013. Архивировано[https://web.archive.org/web/20131222172
431/https://wiki.python.org/jython/WhyJython] 22 декабря 2013 года.
10. ↑ IronPython[https://wiki.python.org/moin/IronPython]. Python Wiki. Дата
обращения: 4 апреля 2011. Архивировано[https://web.archive.org/web/2011061204115
8/http://wiki.python.org/moin/IronPython] 12 июня 2011 года.
11. ↑ [https://web.archive.org/web/20131224175835/http://bitbucket.org/pypy/pypy
/raw/stm-thread/pypy/doc/stm.rst Архивная
копия[https://bitbucket.org/pypy/pypy/raw/stm-thread/pypy/doc/stm.rst] от 24
декабря 2013 на Wayback Machine[/wiki/Wayback_Machine] PyPy-STM on
Bitbucket[/wiki/Bitbucket]]
12. ↑ Update on STM[http://morepypy.blogspot.ru/2013/10/update-on-stm.html].
Python Wiki (16 октября 2013). Дата обращения: 21 декабря 2013. Архивировано[htt
ps://web.archive.org/web/20131224111112/http://morepypy.blogspot.ru/2013/10/upda
te-on-stm.html] 24 декабря 2013 года.



```

2. https://www.rbc.ru/society/09/07/2023/64aa78c89a794719e603638f

```
	
                    В Сочи закрыли все пляжи из-за ливней, града и смерчей

                

Все городские пляжи в Сочи закрыты в связи с непогодой, сообщила администрация
курорта. В городе продолжает действовать штормовое предупреждение.

«Возможно выпадение большого количества осадков с градом. На реках вероятны
резкие подъемы уровней воды до неблагоприятных отметок. Имеется опасность
формирования смерчей над морем», — сообщили в администрации.

Департамент курортов, туризма и потребительской сферы администрации города
уточнил, что купание в Сочи запрещено до 11 июля.

Резкое ухудшение погоды произошло в городе вчера, когда на курорт обрушились
проливные дожди и ветер. Потоки воды, по данным МЧС,
снесли[https://www.rbc.ru/rbcfreenews/64aa633e9a7947a975b3edc2] больше десятка
автомобилей. В Хостинском районе оказались затоплены несколько жилых домов, из
одного часть жителей отселили в пункт временного размещения. Никто не пострадал.
Всего в ночь на 9 июля в городе выпало около 80 мм осадков, сильные дожди
ожидаются и в ночь на 10 июля.

                                                      Video

Непогода обрушилась и на Краснодар. Накануне там затоплены оказались улицы
Одесская, Рашпилевская, Ростовское шоссе, улица Фадеева, Северная, Московская,
Дальняя, Атарбекова и Коммунаров. Из-за ливня остановились трамваи и
троллейбусы, позднее движение возобновили. Синоптики
объявляли[https://kuban.rbc.ru/krasnodar/freenews/64a9779b9a794723805a1d8a]
штормовое предупреждение, в регионе с 7 по 9 июля прогнозировался сильный дождь
с грозой, градом и шквалистым ветром до 20–23 м/с.

Будущее можно увидеть, но оно еще не предрешено

Хватит ли у тебя смелости узнать, что скрывает полынь?

Включи лето на максимум. Смотри все серии на KION

Добро пожаловать в другой мир

Реклама, ПАО "МТС", ОГРН: 1027700149124  109147, ГОРОД МОСКВА, УЛ. МАРКСИСТСКАЯ,
Д.4, 16+



```

3. https://lenta.ru/news/2023/06/05/vvozdukh.html

```
  00:27, 5 июня 2023
  Власти США подняли истребители в воздух из-за пролетевшего бизнес-джета

Власти США[/tags/geo/ssha/] подняли в воздух истребители из-за пролетевшего
бизнес-джета Cessna Citation, который нарушил воздушное пространство над
Вашингтоном[/tags/geo/vashington/] и упал в соседнем штате Вирджиния. Об этом
сообщает агентство Reuters[https://www.reuters.com/], ссылаясь на собственные
источники.Как уточняется, воздушное судно было на автопилоте и не реагировало на
предупреждения властей. По словам собеседников агентства, действия истребителей
не были причиной падения бизнес-джета.В это же время жители Вашингтона и
окрестностей услышали[https://lenta.ru/news/2023/06/04/virdzhinia/] громкий
звук. Изначально представители пожарной службы и службы внутренней безопасности
в Вашингтоне опровергли сообщения о каких-либо инцидентах в городе. Позже
Журналисты Reuters подчеркнули, что звук был связан с произошедшим.22 мая власти
США опровергли[https://lenta.ru/news/2023/05/22/pentagon_no_blast/] сообщения о
взрыве возле Министерства обороны США[/tags/organizations/pentagon/]. Так
представитель Пентагона отреагировал на ряд публикаций в соцсетях, которые
сопровождались снимком, якобы сделанным возле здания ведомства.Ранее появилось
множество публикаций, в которых говорилось о мощном взрыве возле Пентагона.
Многие из них сопровождались одним и тем же фото с большим столбом черного дыма.
```

4. https://ria.ru/20230709/gaz-1883102033.html

```
14:14 09.07.2023
                                (обновлено: 18:02 09.07.2023)
                            
  Россия стала главным поставщиком газа в Испанию в июне

МОСКВА, 9 июл — РИА Новости. По итогам июня Россия стала первым по объемам
поставщиком газа в Испанию, следует из данных энергетической компании
Enagas[https://www.enagas.es/en/]. Так, за месяц Испания импортировала из России
7673 гигаватт-часа сжиженного природного газа, что составило 26,8 процента от
общего объема закупок. С января по июнь Испания закупила у России 41 145
гигаватт-часов СПГ. В Австрии заявили об отсутствии альтернативы поставкам
российского газа1 июля,
09:35[https://ria.ru/20230701/avstriya-1881612327.html?in=t]Второе место после
России занимает Алжир, экспортировавший в Испанию 21 процент от общего объема
газа, а третье — США, на долю которых пришлось 18,5 процента. В начале года
импорт российского газа в Испанию увеличился на 151 процент — если в феврале
2022-го он составлял 2174 гигаватт-часа, то год спустя вырос до 5465 (17,2
процента от общего объема поставок).При этом в марте испанские власти призвали
импортеров не подписывать новые контракты с Москвой[/location_Moskva/] и
активизировать диверсификацию поставок СПГ. На сегодняшний день Испания
позиционирует себя как крупный газовый хаб, способный разрешить европейский
энергетический кризис, вызванный сокращением поставок российского топлива.
Причем подчеркивается, что она располагает наиболее диверсифицированным списком
поставщиков: с начала года экспортерами газа в Испанию выступили более 20
стран."Газпром" и CNPC обсудили поставки газа в Китай16 июня,
21:34[https://ria.ru/20230616/postavki-1878799395.html?in=t]
```