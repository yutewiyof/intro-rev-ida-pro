# Часть 50

## РАБОТА С ЯДРОМ WINDOWS

Смысл этого туториала состоит в том, чтобы создать небольшой гайд по реверсингу и отладке ядра. Я не думаю, что очень важно делать очень подробное введение про то, что такое ядро. Для этого есть тысяча туториалов. Но несмотря на это я скопирую эти определения.

**KERNEL** или **ЯДРО** это **фундаментальный компонент любой операционной системы**. Оно отвечает за то, что программное обеспечение и аппаратное обеспечение любого компьютера может работать вместе в той же системе, для чего оно управляет памятью программ и исполняемых процессов, управляет временем процессора, который используют программы, или заботится о предоставлении доступа и правильной работе периферических устройств и других физических элементов оборудования.

![](.gitbook/assets/50/01.png)

Мы видим, что в режиме пользователя находятся приложения, функции **API WINDOWS**, драйвера, которые обрабатываются в режиме пользователя, в то время как в режиме ядра находится сама операционная система, аппаратное обеспечение и драйвера, которые работают в режиме ядра.

Когда ты запускаешь приложение, оно входит в режим пользователя, где **WINDOWS** создает конкретный процесс для приложения. Каждое приложение имеет свой защищенный виртуальный адрес. Ничто не может изменить данные, которые принадлежат другому процессу и не имеет доступа к виртуальному пространству самой операционной системы. Следовательно, это **режим, который предоставляет меньше привилегий**. Даже доступ к аппаратному обеспечению ограничен, и для вызова сервисов системы приложения должны прибегать к **API WINDOWS**.

Режим ядра или **KERNEL** по другому — это то место, где **код который выполняется, имеет прямой доступ ко всему аппаратному обеспечению** и всей памяти оборудования. Здесь весь код делит то же адресное пространство, и может даже получать доступ в адресные пространства всех процессов режима пользователя. Это опасно, так как если драйвер в режиме ядра изменит то, что не должен, то это может повлиять на работу всей операционной системы.

Этот режим ядра **состоит из исполнительных сервисов**, таких как контроллер кэша, диспетчера связи, диспетчера В/В, локальных вызовов процедур, или диспетчеров электропитания и памяти. Они, в свою очередь, формируются из нескольких модулей, которые выполняют конкретные задачи, контроллеры ядра, ядро и Слой Абстрагирования Оборудования или **HAL**.

Мы продолжаем копировать определения. Сейчас идет определение виртуальной памяти.

Виртуальная память - это техника используемая операционными системами **для доступа к большему количеству памяти чем физически доступно. ОС** прибегает к альтернативным решениям хранения данных, когда иссякает установленная память **RAM**.

Компьютеры используют память **RAM** для хранения файлов и данных, которые необходимы как операционной системе так и программному обеспечению, которое мы запускаем; её высокая производительность гарантирует оптимальную производительность но, рано или поздно, она всегда заполняется. Именно в этот момент **WINDOWS** прибегает к **виртуальной памяти**.

Для создания виртуальной памяти **WINDOWS** создаёт файл в хранилище, которые мы назначаем, будь то на традиционном жестком диске или **SSD**; операционная система генерирует файл под названием **PAGEFILE.SYS** \(вы можете найти его скрытым в корневой директории вашей системы\) где она хранит данные, которые не помещаются в память **RAM**, но которые необходимы для работы **ПК**.

## PIC

Поскольку, когда мы работаем с очень требовательными приложениями \(такими как видеоигры\) или у нас есть несколько одновременно работающих приложений, Вы можете заметить как система начинает замедляться, особенно если у **ПК** недостаточно памяти **RAM**. Это тот самый момент, когда **WINDOWS** начинает задействовать файл подкачки и память **RAM** будет переполнена; поэтому предотвращаются сбои и нестабильность, но вместо этого снижается производительность.

На этом месте, легко сделать вывод, **что чем больше RAM мы имеем в оборудовании**, тем лучше мы заметим разницу в более требовательном программном обеспечении, которое мы используем. Хотя цена памяти в последнее время резко упала, она остается по-прежнему высокой. Поэтому в большинстве случаев необходимо прибегать к решениям оперативной памяти.

![](.gitbook/assets/50/03.png)

Здесь мы видим виртуальное адресное пространство каждого процесса, который начинается от адреса **0x0** до **0xFFFFFFFF** и которое операционная система использует для управления **RAM** и **SWAP**как мы говорили ранее.

![](.gitbook/assets/50/04.png)

И также видим **32**-х битное виртуальное адресное пространство каждого процесса, которое разделяется. Как мы видим на картинке от адреса **0x0** до **0x7FFFFFFF** это часть пользовательского пространства где располагаются программы и от адреса **0x7FFFFFFF** до **0xFFFFFFFF** это пространство ядра.

Хорошо. Давайте перестанем воровать с Интернета инфу и подготовим гайд. Очевидно мы не можем отлаживать ядро с помощью отладчика типа **OLLYDBG** или **IDA** в режиме пользователя, потому что они не могут получить доступ как любая программа в режиме пользователя, в часть ядра.

Мы должны подготовить целевую машину где будем отлаживать ядро. В моём случае, я использую **VMWARE WORKSTATION** и у меня есть моя целевая машина **WINDOWS 7 SP1 32**, без каких либо обновлений.

Те, кто использует более обновленные целевые машины могут обнаружить, что некоторые вещи не будут работать соответствующим образом, потому что машины пропатчены. Но поскольку мы начинаем с самого начала, лучше видеть всё проще и продвигаться постепенно.

Как только мы подготовим окружающую среду, возможно, что мы продолжим позже с **ВИДЕО ТУТОРИАЛАМИ**, поэтому важно все хорошо подготовить, чтобы идти дальше нормально.

Моя основная машина, в этом случае, это **WINSOWS 7 SP1 64**, со всеми патчами до сегодняшнего дня. Хотя мы могли бы использовать другую систему, может случиться, что кое-какая вещь не будет работать точно также как у меня, но такое может случиться и так.

В моей основой машине, я буду использовать **IDA** версии **6.8**. И прежде чем, вы закричите, что уже в сеть утекла **IDA 7**, я скажу, что она имеет баг, который закрывает программу при попытке присоединения отладчика для отладки **32-х** битного ядра. Поскольку в моей работе мне покупают **IDA** официально, разработчики прислали мне патч, который устраняет этот баг. Но очевидно я не могу распространять его. Возможно кто-то найдет место из-за чего падает программа и поймет как избежать это и пофиксит его и получить валидный патч для **IDA 7**. Но пока мы будем использовать версию **6.8**.

Конечно, также основная машина должна иметь установленный **WINDBG** и настроенные символы. И обратите внимание, что в этой папке символов, в том время, когда используем их, они скачиваются сами. В моём случае папка называется **SYMBOLS**.

![](.gitbook/assets/50/05.png)

Поскольку в моих переменных среды есть переменная **\_NT\_SYMBOL\_PATH**

![](.gitbook/assets/50/06.png)

Её значение равно

>**SRV\*c:\symbols\***[**http://msdl.microsoft.com/download/symbols**](http://msdl.microsoft.com/download/symbols)

И эта строка позволяет загружать символы с сервера microsoft. Очевидно Вам нужно что-то сделать, чтобы отладчик смог подключаться через фаерволлы, прокси или чего нибудь ещё, чтобы получить доступ к репозиторию символов.

Следующая вещь - необязательна. На моей главной машине у меня есть, т.е. на машине с **WINDOWS 7**, установлен старый **WDK 7.1.0** [**https://www.microsoft.com/en-us/download/details.aspx?id=11800**](https://www.microsoft.com/en-us/download/details.aspx?id=11800)

Но на другой машине, на которой у меня установлен **WINDOWS 10**, чтобы стараться делать те же самые вещи, у меня есть установленная **VISUAL STUDIO 2015** с **WDK 10** поскольку на данный момент **VISUAL STUDIO 2017** не позволяет использовать **WDK**.

У меня есть две возможности сделать это. С помощью обоих методов нужно компилировать драйвер по старинке вручную в текстовом редакторе \(красивый\) или по-современному. И увидем, работает ли этот способ и посмотрим различая.

Чтобы протестировать драйверы нужно перейти по ссылке [**http://www.osronline.com/article.cfm?article=157**](http://www.osronline.com/article.cfm?article=157)

Зарегистрируйтесь и загрузите **OSR DRIVER LOADER**, который поможет нам легко загрузить и протестировать наш драйвер.

Загрузите также **DEBUG VIEW** с сайта **MICROSOFT**

[**https://docs.microsoft.com/en-us/sysinternals/downloads/debugview**.](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview.)

И как только у нас будут всё эти инструменты, мы загружаем **VIRTUAL KD**

[**http://virtualkd.sysprogs.org/download/**](http://virtualkd.sysprogs.org/download/)

В этот момент последняя версия это **3**. Если выйдет более новая, не забудьте её скачать.

После само-распаковки видно

![](.gitbook/assets/50/07.png)

![](.gitbook/assets/50/08.png)

Видно, что существует папка **TARGET**, которая является той, которую нужно скопировать в целевую машину. Остальная часть файлов предназначена для основной машины.

После этого я копирую папку **TARGET** в целевую машину.

![](.gitbook/assets/50/09.png)

И запускаю **VMINSTALL** с правами администратора.

![](.gitbook/assets/50/10.png)

Эту галочку я тестировал несколько раз и если я не снимал её в **WINDOWS 7**, то ничего не работало. В любом случае, всё равно можно сделать снимок, чтобы сделать тест и если ничего не заработает, вернуться назад к снимку и повторить попытку.

Перед тем как нажать **INSTALL**, скопируйте имя и вставьте его в блокнот на основной машине. Теперь я снимаю галочку и нажимаю **INSTALL**.

![](.gitbook/assets/50/11.png)

![](.gitbook/assets/50/12.png)

Заметьте, что если всё правильно, машина будет оставаться замороженной при запуске. Это то, что должно случиться, иначе что-то установленно неправильно. Перед тем как нажимать **YES**, давайте запустим в основной машине другую часть **VIRTUALKD**. Я выполняю с правами администратора **VMMON64.EXE**. После того как файл запуститься, давайте вернемся назад и нажмем **YES**.

![](.gitbook/assets/50/13.png)

Здесь мне будет представлена возможность запустить машину в нормальном режиме или запустить в режиме отладки ядра, что является выделенным на картинке. Если я соглашаюсь и машина запускается нормально не работает, но иногда не обязательно устанавливать все заново. Когда она загружается, я приказываю ей перегрузиться и выбираю тот же самый пункт, чтобы увидеть зависнет ли она снова.

Поскольку моя машина запускается нормально, я не восстанавливаю ничего.

![](.gitbook/assets/50/14.png)

Я пытаюсь запустить этот **REG** файл и затем вернуться обратно в **VMINSTALL**, чтобы увидеть заработал ли он сейчас.

При перезагрузке он запускается. На главной машине, если в программе **VMMON64** не находится слово **YES** под колонкой **OS**, это значит что что-то не так.

![](.gitbook/assets/50/15.png)

После нескольких попыток и нескольких перезапусков, я думаю, что трюк состоит в том, чтобы перегружать целевую машину из самой системы, а не из меню **VMWARE**. Если всё работает, должно случиться это.

![](.gitbook/assets/50/16.png)

Целевая машина должна быть заморожена в самом начале.

![](.gitbook/assets/50/17.png)

Здесь под словом **OS** должно находиться слово **YES** и если Вы установите галочку на **START DEBUGGER AUTOMATICALLY** должен запускаться **WINDBG**. Но в **DEBUGGER PATH** вы должны указать корректный путь до **WINDBG.EXE**, тогда он запуститься,

![](.gitbook/assets/50/18.png)

Мы вводим **G**, и **ENTER** в **WINDBG** и отладчик продолжит загружать систему. Как только я войду в целевую машину, то я возвращаюсь в **WINDBG** и нажимаю **BREAK** из меню **DEBUG** или **CTRL** + **BREAK**.

![](.gitbook/assets/50/19.png)

Там я исполняю команду `!PROCESS -1 0`

```console
kd> !process -1 0
PROCESS 83fc4a20 SessionId: none Cid: 0004 Peb: 00000000 ParentCid: 0000
DirBase: 00185000 ObjectTable: 87c01a88 HandleCount: 466.
Image: System
```

Я нахожусь в командной строке. Посмотрим список процессов с помощью команды `!PROCESS 0 0`

```console
kd> !process 0 0
**** NT ACTIVE PROCESS DUMP ****
PROCESS 83fc4a20 SessionId: none Cid: 0004 Peb: 00000000 ParentCid: 0000
DirBase: 00185000 ObjectTable: 87c01a88 HandleCount: 466.
Image: System

PROCESS 8502b3f8 SessionId: none Cid: 010c Peb: 7ffdd000 ParentCid: 0004
DirBase: 3ec2d020 ObjectTable: 88c1f178 HandleCount: 29.
Image: smss.exe

PROCESS 85771d40 SessionId: 0 Cid: 016c Peb: 7ffdf000 ParentCid: 0164
DirBase: 3ec2d060 ObjectTable: 96a4b590 HandleCount: 504.
Image: csrss.exe

PROCESS 856cd530 SessionId: 0 Cid: 0194 Peb: 7ffdf000 ParentCid: 0164
DirBase: 3ec2d0a0 ObjectTable: 96a4d5e0 HandleCount: 75.
Image: wininit.exe

PROCESS 856f6530 SessionId: 1 Cid: 019c Peb: 7ffdd000 ParentCid: 018c
DirBase: 3ec2d040 ObjectTable: 96a52b10 HandleCount: 179.
Image: csrss.exe

PROCESS 8573e530 SessionId: 1 Cid: 01d8 Peb: 7ffd6000 ParentCid: 018c
DirBase: 3ec2d0c0 ObjectTable: 96b9c620 HandleCount: 108.
Image: winlogon.exe

PROCESS 859ad030 SessionId: 0 Cid: 0208 Peb: 7ffdf000 ParentCid: 0194
DirBase: 3ec2d080 ObjectTable: 96a52ac8 HandleCount: 216.
Image: services.exe

PROCESS 84fbd9b0 SessionId: 0 Cid: 0218 Peb: 7ffdb000 ParentCid: 0194
DirBase: 3ec2d0e0 ObjectTable: 87cc3268 HandleCount: 556.
Image: lsass.exe

PROCESS 859c1030 SessionId: 0 Cid: 0220 Peb: 7ffdc000 ParentCid: 0194
DirBase: 3ec2d100 ObjectTable: 96b610d8 HandleCount: 141.
Image: lsm.exe

PROCESS 85a42708 SessionId: 0 Cid: 0278 Peb: 7ffdd000 ParentCid: 0208
DirBase: 3ec2d120 ObjectTable: 81f66f58 HandleCount: 352.
Image: svchost.exe

PROCESS 85a55030 SessionId: 0 Cid: 02b0 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d140 ObjectTable: 81faf9d8 HandleCount: 53.
Image: vmacthlp.exe

PROCESS 85a69030 SessionId: 0 Cid: 02d8 Peb: 7ffdd000 ParentCid: 0208
DirBase: 3ec2d160 ObjectTable: 81f699c8 HandleCount: 267.
Image: svchost.exe

PROCESS 8596e928 SessionId: 0 Cid: 0350 Peb: 7ffd4000 ParentCid: 0208
DirBase: 3ec2d1a0 ObjectTable: 81f769d8 HandleCount: 412.
Image: svchost.exe

PROCESS 85abc030 SessionId: 0 Cid: 0378 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d1c0 ObjectTable: 8a6a1e98 HandleCount: 397.
Image: svchost.exe

PROCESS 85ac2030 SessionId: 0 Cid: 0394 Peb: 7ffd9000 ParentCid: 0208
DirBase: 3ec2d1e0 ObjectTable: 8a6ab3b0 HandleCount: 1027.
Image: svchost.exe

PROCESS 85b234b8 SessionId: 0 Cid: 0434 Peb: 7ffd6000 ParentCid: 0208
DirBase: 3ec2d200 ObjectTable: 8a6d6a08 HandleCount: 536.
Image: svchost.exe

PROCESS 85b5ec88 SessionId: 0 Cid: 0484 Peb: 7ffda000 ParentCid: 0208
DirBase: 3ec2d220 ObjectTable: 8a73fb70 HandleCount: 376.
Image: svchost.exe

PROCESS 85710148 SessionId: 0 Cid: 04f0 Peb: 7ffd8000 ParentCid: 0208
DirBase: 3ec2d240 ObjectTable: 81fac1b8 HandleCount: 335.
Image: spoolsv.exe

PROCESS 8571e030 SessionId: 0 Cid: 0514 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d260 ObjectTable: 91405ec8 HandleCount: 334.
Image: svchost.exe

PROCESS 85c02900 SessionId: 0 Cid: 05b0 Peb: 7ffdd000 ParentCid: 0208
DirBase: 3ec2d280 ObjectTable: 93cf2628 HandleCount: 83.
Image: VGAuthService.exe

PROCESS 85c12bb8 SessionId: 0 Cid: 05dc Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d2a0 ObjectTable: 81ef5558 HandleCount: 291.
Image: vmtoolsd.exe

PROCESS 85c4d610 SessionId: 0 Cid: 06d0 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d2c0 ObjectTable: 9168ae58 HandleCount: 101.
Image: svchost.exe

PROCESS 85761d40 SessionId: 0 Cid: 076c Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d2e0 ObjectTable: 8a6a59f8 HandleCount: 192.
Image: dllhost.exe

PROCESS 85cc7c48 SessionId: 0 Cid: 0790 Peb: 7ffd8000 ParentCid: 0278
DirBase: 3ec2d300 ObjectTable: 8a78a190 HandleCount: 191.
Image: WmiPrvSE.exe

PROCESS 85cdc658 SessionId: 0 Cid: 07d8 Peb: 7ffd5000 ParentCid: 0208
DirBase: 3ec2d340 ObjectTable: 916705d8 HandleCount: 191.
Image: dllhost.exe

PROCESS 85d3fa30 SessionId: 0 Cid: 0190 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d320 ObjectTable: 9175c2c8 HandleCount: 152.
Image: msdtc.exe

PROCESS 85075cb0 SessionId: 0 Cid: 0528 Peb: 7ffdc000 ParentCid: 0208
DirBase: 3ec2d360 ObjectTable: 916c0a70 HandleCount: 110.
Image: VSSVC.exe

PROCESS 84e9b030 SessionId: 0 Cid: 0784 Peb: 7ffd4000 ParentCid: 0278
DirBase: 3ec2d380 ObjectTable: 917d4938 HandleCount: 318.
Image: WmiPrvSE.exe

PROCESS 8570d538 SessionId: 1 Cid: 0858 Peb: 7ffdc000 ParentCid: 0208
DirBase: 3ec2d3e0 ObjectTable: 96b75ba0 HandleCount: 156.
Image: taskhost.exe

PROCESS 85e58030 SessionId: 0 Cid: 08f4 Peb: 7ffdc000 ParentCid: 0208
DirBase: 3ec2d440 ObjectTable: 91d3ddd8 HandleCount: 166.
Image: sppsvc.exe

PROCESS 85af2b08 SessionId: 1 Cid: 0974 Peb: 7ffdc000 ParentCid: 0378
DirBase: 3ec2d180 ObjectTable: 9175b340 HandleCount: 68.
Image: dwm.exe

PROCESS 85e626f0 SessionId: 1 Cid: 0980 Peb: 7ffdb000 ParentCid: 096c
DirBase: 3ec2d460 ObjectTable: 81ef1540 HandleCount: 600.
Image: explorer.exe

PROCESS 85ea28f8 SessionId: 1 Cid: 09e0 Peb: 7ffd5000 ParentCid: 0980
DirBase: 3ec2d420 ObjectTable: 9482bc18 HandleCount: 33.
Image: jusched.exe

PROCESS 85ea9030 SessionId: 1 Cid: 09e8 Peb: 7ffd5000 ParentCid: 0980
DirBase: 3ec2d400 ObjectTable: 94823c00 HandleCount: 225.
Image: vmtoolsd.exe

PROCESS 84061298 SessionId: 0 Cid: 0a88 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d4a0 ObjectTable: 91f99d78 HandleCount: 630.
Image: SearchIndexer.exe

PROCESS 840685a0 SessionId: 0 Cid: 0aec Peb: 7ffd6000 ParentCid: 0a88
DirBase: 3ec2d480 ObjectTable: 91f65210 HandleCount: 312.
Image: SearchProtocolHost.exe

PROCESS 840758b8 SessionId: 0 Cid: 0b00 Peb: 7ffd5000 ParentCid: 0a88
DirBase: 3ec2d4c0 ObjectTable: 949d8b40 HandleCount: 78.
Image: SearchFilterHost.exe

PROCESS 84ea7030 SessionId: 0 Cid: 0c14 Peb: 7ffdb000 ParentCid: 0208
DirBase: 3ec2d3c0 ObjectTable: 954c8948 HandleCount: 312.
Image: svchost.exe

PROCESS 840d3d40 SessionId: 0 Cid: 0e00 Peb: 7ffdf000 ParentCid: 0208
DirBase: 3ec2d3a0 ObjectTable: 94822518 HandleCount: 117.
Image: WmiApSrv.exe
```

Это список процессов. Если я хочу переключиться на контекст другого процесса, чтобы поставить там **BP**, я бы сделал так.\(Например переключиться на **EXPLORER**, который в моем случае имеет адрес **85E626F0** рядом со словом **PROCESS**\)

```console
kd> .process /i 85e626f0
You need to continue execution \(press 'g' <enter>\) for the context
to be switched. When the debugger breaks in again, you will be in
the new process context.
```

Я нажимаю **G** и контекст переключается

```console
kd> g
Break instruction exception - code 80000003 \(first chance\)
nt!RtlpBreakWithStatusInstruction:
82676394 cc
```

Я вижу в каком процессе я нахожусь сейчас

```console
kd> !process -1 0
PROCESS 85e626f0 SessionId: 1 Cid: 0980 Peb: 7ffdb000 ParentCid: 096c
DirBase: 3ec2d460 ObjectTable: 81ef1540 HandleCount: 600.
Image: explorer.exe
```

Если Вы не хотите тратить время, Вы можете пропустить загрузку символов в этот момент. Поскольку это только для практики, то потребуется много времени. Если вы хотите продолжить, перейдите на следующую страницу, где заканчивается пунктирная область.

* * *

Я перегружаю символы с помощью команды **.RELOAD /F**

Это будет занимать какое-то время. Некоторые символы будут скачаны сами, потому что они находятся в репозитории. Некоторые модули не будут иметь символов. Но папка символом должна быть заполнена.

![](.gitbook/assets/50/20.png)

Здесь мы видим, что **WINDBG** находится в состоянии **BUSY** и загружает символы \(скачивает\). Первый раз, когда мы это сделаем, это будет очень долго, потому что у программы нет символов. Следующие разы не будут являться для нас такой проблемой.

Если программа не загрузила символы, вы можете использовать команду `!SYM NOISY` перед `RELOAD`.

Run !sym noisy before .reload to track down problems loading symbols.

* * *

Многие спросят, если это курс **IDA**, почему мы не присоединяемся сразу в начале загрузки **IDA** с помощью плагина **WINDBG**.

Смысл в том, что **WINDBG** я использую для того, чтобы добраться до нужной точки, где я хочу отлаживать и как только я её достигаю я присоединяюсь с помощью **IDA**, потому что **IDA** иногда падает и всё подвисает, поэтому лучше использовать и доходить до интересующей точки c помощью **WINDBG**, отлаживать и покидать **WINDBG** в неинтересующей части, что является более надежным способ для удаленной отладки ядра. В любом случае, я могу прерваться, закрыть **WINDBG** и целевая система останется заморожена и потом присоединить **IDA** с плагином **WINDBG** и продолжить отладку без проблем. Это мы и сделаем дальше.

Если Вы перезагрузили с помощью команды **LM**, Вы увидите модули и их символы

```console
kd> LM
start end module name
00550000 007d0000 Explorer (pdb symbols) c:\symbols\explorer.pdb\A289F16DBCB94B618103DE843592AB182\explorer.pdb
6bd50000 6bda2000 zipfldr (pdb symbols) c:\symbols\zipfldr.pdb\0CFC61030167490C9ABF25C441E651D11\zipfldr.pdb
6bdb0000 6bddb000 provsvc (pdb symbols) c:\symbols\provsvc.pdb\222401C8EF0749BA9E532D6AA6666F601\provsvc.pdb
6bde0000 6be2f000 hgcpl (pdb symbols) c:\symbols\hgcpl.pdb\4EA31C513A1C47F78EAAC3A5CD54D59A1\hgcpl.pdb
6be90000 6bf73000 FXSRESM (no symbols)
6bf80000 6bfe4000 imapi2 (pdb symbols) c:\symbols\imapi2.pdb\4F52351C2B514C3699D1B47D48BCFA322\imapi2.pdb
6bff0000 6c02a000 FXSAPI (pdb symbols) c:\symbols\FXSAPI.pdb\C5C8AC671FA34D9EB1CDD55364F6E39E2\FXSAPI.pdb
6c030000 6c102000 fxsst (pdb symbols) c:\symbols\FXSST.pdb\DDFADEC7308347E9AD60E0617335C84D2\FXSST.pdb
6c110000 6c31e000 SyncCenter (pdb symbols) c:\symbols\SyncCenter.pdb\23C05D457D6F4BA8AAB78F8293F398C92\SyncCenter.pdb
6c320000 6cd9c000 ieframe (pdb symbols) c:\symbols\ieframe.pdb\BAAAEB87C2F8485C80589CCF7E3A82BE2\ieframe.pdb
6cda0000 6ce50000 bthprops (pdb symbols) c:\symbols\bthprops.pdb\97B2FBEB35D64296B802DD2387D5E1CF1\bthprops.pdb
6ce50000 6ce98000 wwanapi (pdb symbols) c:\symbols\wwanapi.pdb\9862E0172237487BBFEF6C1B3EBEE58A1\wwanapi.pdb
6cf70000 6d02a000 Actioncenter (pdb symbols) c:\symbols\ActionCenter.pdb\98A49FC8D39C471996BEB3EF01EAA4831\ActionCenter.pdb
6d340000 6d4ee000 pnidui (pdb symbols) c:\symbols\pnidui.pdb\50126007BD354C589514BA7F546EA17A2\pnidui.pdb
6d4f0000 6d755000 netshell (pdb symbols) c:\symbols\netshell.pdb\083CF46E903F426AA06FF633605370E32\netshell.pdb
6d8c0000 6d8ee000 QAgent (pdb symbols) c:\symbols\qagent.pdb\ABAFFF300B6A48789369D4A90AD2DC222\qagent.pdb
6da60000 6da76000 Wlanapi (pdb symbols) c:\symbols\wlanapi.pdb\48EE3C9420F24448833370695E2AF4772\wlanapi.pdb
6df90000 6df9a000 wwapi (pdb symbols) c:\symbols\wwapi.pdb\84C82A03729E48E0A883E55B56B7A0161\wwapi.pdb
6e1e0000 6e1eb000 CSCAPI (pdb symbols) c:\symbols\cscapi.pdb\3D7C1EEDC26B43C6B4CFD2BBF8EE08CB2\cscapi.pdb
```

Те модули, у которых есть символы, они сохраняются в мою папку **SYMBOLS**. Это означает, что все хорошо настроено, а если нет, то пусть Билл Гейтс поплачет.

Я буду делать простой тестовый драйвер типа **HELLO WORLD** на основной машине. Тот, кто не хочет его компилировать, он будет находиться в папки туториала.

В папке, которая не имеет пробелов ни в имени, ни в пути, я создаю текстовый файл и размещаю внутри него следующий код.

```c
#include <ntddk.h>

void DriverUnload(
PDRIVER_OBJECT pDriverObject)
{
    DbgPrint("Driver unloadingn");
}

NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath)
{
    DriverObject->DriverUnload = DriverUnload;

    DbgPrint("Hello, Worldn");

    return STATUS_SUCCESS;
}
```

Я переименовываю его как **HELLOWORLDDRIVER.C**. Затем сделаю другой файл, который называется **SOURCES** с таким содержанием.

```txt
TARGETNAME = HelloWorldDriver
TARGETPATH = obj
TARGETTYPE = DRIVER

INCLUDES = %BUILD%\inc
LIBS = %BUILD%\lib

SOURCES = HelloWorldDriver.c
```

И ещё один, который называется **MAKEFILE.DEF**

```def
!INCLUDE $(NTMAKEENV)\makefile.def
```

Чтобы скомипилировать его, если я установил **DWK 7.1**, я иду в панель установленных программа **WINDOWS** на главной машине.

![](.gitbook/assets/50/21.png)

И я запускаю **X86 FREE BUILD ENVIRONMENT** из **WINDOWS 7**.

![](.gitbook/assets/50/22.png)

Здесь я меняю путь, чтобы он был без пробелов, где находятся **3** файла.

![](.gitbook/assets/50/23.png)

Я выполняю команду **BUILD**.

![](.gitbook/assets/50/24.png)

Файлы компилируется.

![](.gitbook/assets/50/25.png)

Чтобы увидеть работает ли драйвер, я копирую файл **SYS** в целевую машину \(если она остановлена в **WINDBG**, я нажимаю **G** и **ENTER** для того, чтобы она запустилась\) и там уже я запускаю **OSRLOADER** с правами администратор. Версия **XP** хорошо работает в **WINDOWS** 7.

![](.gitbook/assets/50/26.png)

![](.gitbook/assets/50/27.png)

Я ищу драйвер и открываю его.

Нажимаю кнопку **REGISTER SERVICE**.

![](.gitbook/assets/50/28.png)

Затем нажимаю **START SERVICE** и если не появляется **BSOD** и выходит то же самое сообщение, значит все хорошо. Чтобы увидеть, то что печатает драйвер, мы должны использовать **DEBUG VIEW** от имени администратор.

![](.gitbook/assets/50/29.png)

И когда я запускаю программу и останавливаю драйвер

![](.gitbook/assets/50/30.png)

Драйвер не может показать вывод на консоль.

В **WINDBG** также видно

![](.gitbook/assets/50/31.png)

Если я нажму **START SERVICE**, то заставляю его работать и прервусь в **WINDBG**.

```console
kd> !process -1 0
PROCESS 83fc4a20 SessionId: none Cid: 0004 Peb: 00000000 ParentCid: 0000
DirBase: 00185000 ObjectTable: 87c01a88 HandleCount: 475.
Image: System
```

Я вижу все процессы с помощью команды **!PROCESS 0 0** и внутри этого списка есть такой

```console
PROCESS 840dd830 SessionId: 1 Cid: 0b28 Peb: 7ffd5000 ParentCid: 0980
DirBase: 3ec2d4c0 ObjectTable: 95585948 HandleCount: 253.
Image: OSRLOADER.exe
```

Я переключаю контекст на него с помощью команды

```console
kd> .process /i 840dd830
You need to continue execution (press 'g' <enter>) for the context
to be switched. When the debugger breaks in again, you will be in
the new process context.
```

Я нажимаю **G** и **ENTER**

Я переключаю контекст

```console
kd> g
Break instruction exception - code 80000003 (first chance)
nt!RtlpBreakWithStatusInstruction:
82676394 cc int 3
```

```console
kd> !process -1 0
PROCESS 840dd830 SessionId: 1 Cid: 0b28 Peb: 7ffd5000 ParentCid: 0980
DirBase: 3ec2d4c0 ObjectTable: 95585948 HandleCount: 253.
Image: OSRLOADER.exe
```

Если мы выполним команду **LM**, увидим, что у нас нет символов для нашего драйвера

`91109000 9110f000 HelloWorldDriver (deferred)`

Поскольку у нас есть файл **PDB**, мы можем заставить отладчик загрузить символы

В папке **SYMBOLS** есть папка с именем **PDB**

![](.gitbook/assets/50/32.png)

Мы добавляем туда папку под названием **HELLOWORLDDRIVER.PDB**

![](.gitbook/assets/50/33.png)

Внутри других папок есть подпапка с различными длинными номерами. Как мы её получаем?

![](.gitbook/assets/50/34.png)

Как только мы создали папку **HELLOWORLDDRIVER.PDB**, мы возвращаемся в **WINDBG** и вводим команду

```console
!sym noisy

.reload /f HelloWorldDriver.sys
```

![](.gitbook/assets/50/35.png)

Отладчик говорит нам имя папки, которую не находит. Мы создаем её, копируя туда **PDB** и затем выполняем команду

`.reload /f HelloWorldDriver.sys`

Затем, с помощью команды **LM** можно увидеть символы. В моём случае файл находится в папке **TEST**.

```console
91109000 9110f000 HelloWorldDriver (private pdb symbols) c:\users\ricnar\desktop\test\objfre\_win7\_x86\i386\HelloWorldDriver.pdb
```

С помощью команды **X** можно увидеть содержимое символов.

```console
kd> x HelloWorldDriver!
9110c004 HelloWorldDriver!__security_cookie_complement = 0x6eeffa5e
9110b000 HelloWorldDriver!KeTickCount = struct _KSYSTEM_TIME
9110c000 HelloWorldDriver!__security_cookie = 0x911005a1
9110d03e HelloWorldDriver!GsDriverEntry (struct _DRIVER_OBJECT *, struct _UNICODE_STRING *)
9110a006 HelloWorldDriver!DriverUnload (struct _DRIVER_OBJECT *)
9110d005 HelloWorldDriver!__security_init_cookie (void)
9110a01a HelloWorldDriver!DriverEntry (struct _DRIVER_OBJECT *, struct _UNICODE_STRING *)
9110a058 HelloWorldDriver! ?? ::FNODOBFM::'string' (<no parameter info>)
9110a046 HelloWorldDriver! ?? ::FNODOBFM::'string' (<no parameter info>)
9110d050 HelloWorldDriver!_IMPORT_DESCRIPTOR_ntoskrnl = <no type information>
9110a040 HelloWorldDriver!DbgPrint (<no parameter info>)
9110b004 HelloWorldDriver!_imp__DbgPrint = <no type information>
9110b008 HelloWorldDriver!ntoskrnl_NULL_THUNK_DATA = <no type information>
9110d064 HelloWorldDriver!_NULL_IMPORT_DESCRIPTOR = <no type information>
```

Там есть адреса и названия . Если мы хотим поставить **BP** в **WINDBG**, стоит это делать находясь контексте процесса.

`bp /p @$proc HelloWorldDriver!DbgPrint`

Вместо **BP HELLOWORLDDRIVER!DRIVERUNLOAD**. Возможно в этом случае это не так важно. Но если этот **BP** установить в системной функции, отладчик будет останавливаться тысячи раз, когда каждый процесс использует эту функцию. В то время как при использовании одиночного-контексного **BP**, только тогда, когда отладчик используется текущий процесс

Давайте посмотрим, работает ли это

```console
kd> **bp /p @$proc HelloWorldDriver!DbgPrint**
```

Сейчас мы запускаем отладчик с помощью **G** и **ENTER**

```console
kd> ba e1 HelloWorldDriver!DbgPrint

kd> g
Breakpoint 2 hit
HelloWorldDriver!DbgPrint:
9111c040 ff2504d01191 jmp dword ptr [HelloWorldDriver!_imp__DbgPrint (9111d004)]
kd> !process -1 0
PROCESS 83fc4a20 SessionId: none Cid: 0004 Peb: 00000000 ParentCid: 0000
DirBase: 00185000 ObjectTable: 87c01a88 HandleCount: 476.
Image: System
```

Здесь я останавливаюсь и вижу, что это функция, которая вызвыает печать. В этом случае, когда я не знаю какой процесс который вызывает функцию, можно поместить **BA E1** или **BP** если конечно отладчик не останавливается много раз как в этом случае.

Хорошо. Сейчас продолжим уже с **IDA**. Для этого мы откроем в **IDA 6.8 HELLOWORLDDRIVER.SYS** и если **PDB** находится в той же папке, она его загрузит. Иначе его будет нужно найти и попросить загрузить.

![](.gitbook/assets/50/36.png)

В **IDA** мы идем в пункт **DEBUGGER → SWITCH DEBUGGER** и выбираем **WINDBG**.

![](.gitbook/assets/50/37.png)

Затем в через **DEBUGGER → DEBUGGER OPTIONS → SET SPECIFIC OPTIONS** мы выбираем пункт **KERNEL MODE DEBUGGING**.

И затем идем в **PROCESS OPTIONS**.

В **CONNECTION STRING** мы помещаем строку соединения с таким содержанием.

```txt
com:port=\.\pipe\kd_[0690]_Windows_Seven_Ultimate_-_i386_-_1,pipe
```

Возьмем имя из **VIRTUALKD**.

![](.gitbook/assets/50/38.png)

![](.gitbook/assets/50/39.png)

Готово. Мы соглашаемся.

Мы замечаем, что **WINDBG** прервался.

![](.gitbook/assets/50/40.png)

И идём в пункт **IDA DEBUGGER → ATTACH TO PROCESS**

![](.gitbook/assets/50/41.png)

Должно показаться слово **KERNEL** и мы соглашаемся. Если этого не будет, значит мы сделали не правильно что-то из предыдущих шагов или машина не может соединиться из-за какой-то ошибки.

Если **IDB** в **IDA** имеет то же самое имя, т.е. мы его не меняем и он по-прежнему продолжает называется **HELLOWORLDDRIVER.IDB**, отладчик должен обнаружить, что он загружает похожий модуль. Мы подтверждаем, что это тот же самый и нажимаем **SAME**

![](.gitbook/assets/50/42.png)

Как только я загрузил драйвер, мы можем начать отлаживать. Где то здесь будет панель **WINDBG** где мы могли бы вводить команды **WINDBG**.

![](.gitbook/assets/50/43.png)

Я могу также ставить **BP** в **IDA**

![](.gitbook/assets/50/44.png)

И здесь у нас сейчас ничего не работает. Запускаем систему командой **G** в **WINDBG**. Я должен нажать **RUN** в **IDA** или **F9**.

Мы видим, что по изображению в целевой машине все заработало и разморозилось. Мы можем запустить и останавливать драйвер как раньше, для того, чтобы он остановился на **BP**.

![](.gitbook/assets/50/45.png)

Здесь мы видим, что всё работает отлично.

На другом компьютере у меня есть **VISUAL STUDIO 2015** с **WDK 10**

![](.gitbook/assets/50/46.png)

Если я скомпилирую его так, чтобы не было ошибок, мне нужно понизить уровень требования или изменить его.

![](.gitbook/assets/50/47.png)

Также в настройках драйвера меняем, что он для **WINDOWS 7**

![](.gitbook/assets/50/48.png)

И при компиляции, он не даёт нам ошибку.
```console

1>------ Rebuild All started: Project: KMDF Driver1, Configuration: Release Win32 ------
1> Building 'KMDF Driver1' with toolset 'WindowsKernelModeDriver10.0' and the 'Desktop' target platform.
1> Stamping Release\KMDFDriver1.inf \[Version\] section with DriverVer=10/27/2017,12.49.58.404
1> Driver.c
1> KMDF Driver1.vcxproj -> c:\Users\rnarvaja\Documents\Visual Studio 2015\Projects\KMDF Driver1\Release\KMDFDriver1.sys
1> KMDF Driver1.vcxproj -> c:\Users\rnarvaja\Documents\Visual Studio 2015\Projects\KMDF Driver1\Release\KMDFDriver1.pdb (Full PDB)
1> Done Adding Additional Store
1> Successfully signed: c:\Users\rnarvaja\Documents\Visual Studio 2015\Projects\KMDF Driver1\Release\KMDFDriver1.sys
1>
1> .........................
1> Signability test complete.
1>
1> Errors:
1> None
1>
1> Warnings:
1> None
1>
1> Catalog generation complete.
1> c:\Users\rnarvaja\Documents\Visual Studio 2015\Projects\KMDF Driver1\Release\KMDF Driver1\kmdfdriver1.cat
1> Done Adding Additional Store
1> Successfully signed: c:\Users\rnarvaja\Documents\Visual Studio 2015\Projects\KMDF Driver1\Release\KMDF Driver1\kmdfdriver1.cat
1>
========== Rebuild All: 1 succeeded, 0 failed, 0 skipped ==========
```

Если я удаляю **BP** и выхожу из **IDA** то целевая машина размораживается.

![](.gitbook/assets/50/49.png)

Я копирую драйвер в целевую машину.

![](.gitbook/assets/50/50.png)

Я ищу сервис, запускаю его и останавливаю, В **DEBUGVIEW** мы видим сообщения. Хотя, очевидно, драйвер не остановится в **IDA**, потому что это другой драйвер, но я могу пойти в **IDA**, чтобы приостановить процесс и пойти в **DEBUGGER DETACH FROM PROCESS** и мы могли бы снова заново присоединить **WINDBG** через **RUN DEBUGGER** в **VMMON** или если нет, открыть новый **SYS** в **IDA** с помощью его **PDB**.

Драйвер немного сложнее чем предыдущий.

![](.gitbook/assets/50/51.png)

Мы заново настраиваем **IDA**, изменяя отладчик на **WINDBG**, оставляя его в режиме ядра и используем ту же строку соединения.

Когда я нажимаю **START**, мне появляется сообщение.

![](.gitbook/assets/50/52.png)

Я говорю отладчику, что это то же самое. Я нажимаю **SAME**.

Я ищу между функциями. Я вижу функцию **\_DRIVERENTRY** и нахожу вызов здесь.

![](.gitbook/assets/50/53.png)

![](.gitbook/assets/50/54.png)

![](.gitbook/assets/50/55.png)

Поэтому я устанавливаю там **BP** и нажимаю **RUN**. Затем я загружаю и выгружаю драйвер и мне появляется сообщение. Если этот то же самое, я говорю ему, что да.

![](.gitbook/assets/50/56.png)

И идет остановка на **BP** как и раньше, но с этой другой версией драйвера.

Это было всего лишь началом, чтобы увидеть как конифигурировать систему для отладки ядра. Возможно следующие туториалы будут в виде видео для посвящения этой теме.

* * *

Автор оригинального текста — Рикардо Нарваха.

Перевод и адаптация на русский язык — Яша Яшечкин.

Перевод специально для форума системного и низкоуровневого программирования - WASM.IN

21.10.2018

Источник:

[**http://ricardonarvaja.info/WEB/INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO/50-INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO%20PARTE%2050.7z**](http://ricardonarvaja.info/WEB/INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO/50-INTRODUCCION%20AL%20REVERSING%20CON%20IDA%20PRO%20DESDE%20CERO%20PARTE%2050.7z)
