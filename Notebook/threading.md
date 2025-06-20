# Threading

| 目錄         | 跳轉                                               | 內容                                                                                                    |
| ------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 前言         | [多執行緒](#Python-多執行緒程序撰寫問題和注意事項) | 單執行緒與多執行緒的差異以及 GIL 的注意事項                                                             |
| 執行面       | [執行面](#執行面-實例)                             | 解釋 threading 套件是如何執行的                                                                         |
| 反例說明     | [反例說明](#執行面注意的反例)                      | 某位作者非常討厭多緒執行，因為容易出錯，所以有舉一些反例或者解決方法去實證                              |
| 資料庫的應用 | [thread 應用 ](#資料庫)                            | 裡面內含資料庫以及網路爬蟲，I/O 方面的請求回覆的時間減輕。 [跳轉 Code](/Notebook/practice_thread.ipynb) |
| 參考資料     | [參考資料](#reference)                             | 所有參考到的資料附在上面                                                                                |

- 前情提要: Python 在執行時，通常是採用同步的任務處理模式 ( 一個處理完成後才會接下去處理第二個 )，然而 Python 的標準函式「threading」採用「執行緒」的方式，運用多個執行緒，在同一時間內處理多個任務 ( 非同步 )，這篇教學會介紹 threading 的用法(同一個步道 vs 不同步道)。

- [About threading](https://docs.python.org/zh-tw/3/library/threading.html)

```python
import threading
```

- 有沒有使用 threading 的差異
  https://steam.oxxostudio.tw/category/python/library/threading.html

$\blue\bigstar$ [回到表目錄](#Threading)

## Python 多執行緒程序撰寫問題和注意事項

- 由於 <mark>GIL</mark> 的存在，Python 的執行緒無法利用多核心的優勢，因此 Python 的執行緒適合用於 I/O 密集型的任務，而不適合用於 CPU 密集型的任務。

  - 事實上但凡有順序性的任務，都不適合使用多執行緒，因為多執行緒的執行，是搶佔方式，並**不保證執行的順序**，而執行緒的切換也會導致效能下降。
  - Python 多執行緒，適合用於 I/O 密集型的任務，例如網路請求，檔案讀寫等等，因為這些任務不強調順序性，且任務的執行時間，大部分都是在等待 I/O 的回應，而不是在執行計算。

    > You could resort to multiprocessing - but as I argue in a previous video, if you need to start scaling your computations beyond one core, you may as well bite the bullet and create a truly distributed and scalable computation engine. In that video I describe a very simple queue/worker approach, but there are many other, more sophisticated ways of doing this as well (Spark, Hadoop, etc.)

    > On the other hand, if your app spends a large portion of its time waiting on many I/O operations to complete (maybe calling an API, a database query, reading/writing files, etc), then properly implemented threading may very well speed up your application. This type of workload is referred to as I/O bound.

- 由於執行緒共享處理程序資源，因此需要注意資源的同步問題，避免資源的競爭問題。`lock`強制等待
  - 如果程式碼中採用的函式或方法不是執行緒安全的，可能會出現因搶佔及執行順序所帶來的程序執行問題。`join`強調順序
  - 因此有非執行緒安全的函式或方法，需要透過加鎖的方式來確保執行緒安全。
  - Python 也提供了一些執行緒安全的函式或方法，例如 queue.Queue 類別，可以用來解決執行緒安全的問題。
- 執行緒共享處理程序資源，需要注意資源的死鎖問題，以及避免資源的競爭問題。
  - 當共享資源的執行緒互相等待對方釋放資源時，可能會導致資源的死鎖問題，因此需要注意資源的死鎖問題，避免資源的競爭問題。

<details>
  <summary><font color=blue>GIL 補充(點擊後展開)</font></summary>

> GIL（Global Interpreter Lock，全域直譯器鎖） 是 Python（特別是 CPython，也就是最常見的 Python 實作）中一個機制: GIL 確保「同一時間只會有一個執行緒在執行 Python bytecode（也就是 Python 解譯器的核心程式碼）」，即使你有多核心 CPU。
> GIL 的設計主要是為了 讓記憶體管理（特別是 reference counting）變得簡單、安全且執行快速，避免需要大量複雜的同步機制。

| 類型       | 是否受 GIL 限制 | 備註                                                | 建議用法           |
| ---------- | --------------- | --------------------------------------------------- | ------------------ |
| I/O 密集型 | ❌ 不受限制     | 因為等待 I/O 時會釋放 GIL，例如：讀寫檔案、網路請求 | threading、asyncio |
| CPU 密集型 | ✅ 有限制       | 多執行緒下無法真正並行運算，效能可能還變差          | multiprocessing    |

[](https://pixnashpython.pixnet.net/blog/post/37296721)

</details>

$\blue\bigstar$ [回到表目錄](#Threading)

## 執行面 (實例)

| 目錄                  | 跳轉                                | 內容                                                         |
| --------------------- | ----------------------------------- | ------------------------------------------------------------ |
| 導入套件              | [link](#導入套件)                   | 簡易的介紹 thread 以及用 function 範例執行                   |
| 執行緒套件說明        | [link](#創建執行緒thread的方法)     | 簡易執行緒套件說明，包含兩個執行緒運作。                     |
| 多執行緒先後          | [link](#有順序-執行緒thread的方法)  | 執行緒的先後問題，用 `join` 解決                             |
| 多執行緒應用          | [link](#Queue-佇列)                 | 將所需要的資料先準備好再一起執行他                           |
| 多執行緒 vs. 單執行緒 | [link](#gilglobal-interpreter-lock) | 比較其運作的效率                                             |
| Lock 鎖住             | [link](#lock-鎖住)                  | 有時候我們會希望一個程序(工作)完整跑完才會進到下一個工作流程 |
| Semaphore 旗標        | [link](#semaphore-旗標)             | 依次放行多少的執行緒進行工作                                 |
| Rlock                 | [link](#rlock)                      | 很多很多的 lock                                              |

| 方法       | 說明                                           |
| ---------- | ---------------------------------------------- |
| start()    | 啟用執行緒。                                   |
| join()     | 等待執行緒，直到該執行緒完成才會進行後續動作。 |
| ident      | 取得該執行緒的標識符。                         |
| native_id  | 取得該執行緒的 id。                            |
| is_alive() | 執行緒是否啟用，啟用 True，否則 False。        |

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### 導入套件

> threading.active_count(): 當前活動中的執行緒數量，也可以寫成 threading.activeCount()
> threading.current_thread: 當前正在使用的執行緒，或寫成 threading.currentThread()
> threading.enumerate(): 當前活動中的所有執行緒資訊

```python
## 導入套件
import threading

def threading_example():
    ## 也可以寫成threading.activeCount()、threading.currentThread()
    print('活動中的執行緒數量: ', threading.active_count())
    print('當前正在使用的執行緒: ', threading.current_thread())
    print('當前正在使用的執行緒名稱: ', threading.current_thread().name)
    print('目前活動中的執行緒資訊: ', threading.enumerate)


if __name__ == '__main__':
    threading_example()
# 活動中的執行緒數量:  6
# 當前正在使用的執行緒:  <_MainThread(MainThread, started 10200)>
# 當前正在使用的執行緒名稱:  MainThread
# 目前活動中的執行緒資訊:  <function enumerate at 0x0000022E60E67380>
```

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### 創建執行緒(thread)的方法

> threading.Thread(target = function, name = '執行敘明稱', args = variable)
> target: 指定執行的函式(工作)
> name: 設定執行緒的名稱
> args: 欲帶入函式的參數，但要以 list 的形式傳入

```python
## 導入套件
import threading

## 新建的執行緒將執行此函數(工作)
def added_thread_job():
    print('新增加的執行緒: ', threading.current_thread())
    print('新增加的執行緒名稱: ', threading.current_thread().name)
    print('活動中的執行緒數量: ', threading.active_count())

## 創建新執行緒
def added_threading_example():
    ## 新稱的執行緒
    added_thread = threading.Thread(target = added_thread_job, name = 'new_added_thread')

    ## 啟動執行緒
    added_thread.start()


if __name__ == '__main__':
    added_threading_example()
# 新增加的執行緒:  <Thread(new_added_thread, started 23444)>
# 新增加的執行緒名稱:  new_added_thread
# 活動中的執行緒數量:  7

import threading

def added_thread_job(a):
    ## 印出傳入的參數
    print(a)

    print('新增加的執行緒: ', threading.current_thread())
    print('新增加的執行緒名稱: ', threading.current_thread().name)
    print('活動中的執行緒數量: ', threading.active_count())

def added_threading_example():
    ## 欲傳入added_thread_job的參數
    text = ['Threading Learning']

    ## 新稱執行緒
    added_thread = threading.Thread(target = added_thread_job, name = 'new_added_thread', args = text)

    ## 啟動執行緒
    added_thread.start()

if __name__ == '__main__':
    added_threading_example()
# Threading Learning
# 新增加的執行緒:  <Thread(new_added_thread, started 16776)>
# 新增加的執行緒名稱:  new_added_thread
# 活動中的執行緒數量:  7
```

- 目前只有一個執行緒的東西。
- 可以用於提示目前在哪一個工作階段 `args` 非常好用，但要用 list 方式回傳。

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### 有順序-執行緒(thread)的方法

> start(): 啟動執行緒，執行工作
> join(): 等到執行緒終止後, 才會往下執行程式碼
> isAlive(): 檢查執行緒是否還在執行
> getName(): 取得 thread 名稱
> setName(): 設定 thread 名稱

```python
import threading

def added_thread_job():
    print('新增加的執行緒: ', threading.current_thread())
    print('新增加的執行緒名稱: ', threading.current_thread().name)
    print('活動中的執行緒數量: ', threading.active_count())

def added_threading_example():
    # 建立執行緒
    added_thread = threading.Thread(target=added_thread_job, name='new_added_thread_1')

    # 設定 thread 名稱（推薦用法）
    added_thread.name = 'new_added_thread_2'

    # 取得 thread 名稱（推薦用法）
    print('指定名稱:', added_thread.name)

    # 啟動執行緒
    added_thread.start()

    # 等待子執行緒結束
    added_thread.join()

    # 檢查執行緒是否仍然存活
    print('子執行緒是否仍活著:', added_thread.is_alive())

if __name__ == '__main__':
    added_threading_example()
# 指定名稱: new_added_thread_2
# 新增加的執行緒:  <Thread(new_added_thread_2, started 24872)>
# 新增加的執行緒名稱:  new_added_thread_2
# 活動中的執行緒數量:  7
# 子執行緒是否仍活著: False
```

- **提醒: 每次執行結果不同，是因為每次執行緒的執行時間可能不同，所以會有先後執行的問題**

```python
## 導入套件
import threading
import time

def added_thread_job():
    print("Thread Start")

    ## 執行工作， 工作內容要執行20次，每次要執行0.1秒，來將執行工作時間拉長
    for i in range(20):
        time.sleep(0.1)
        print('execute job' + str(i))

    print('Thread Finish')

def added_thread_example():
    ## 新建執行緒
    added_thread = threading.Thread(target = added_thread_job, name = 'new_added_thread')

    ## 執行執行緒
    added_thread.start()

    print('Next Code')# ! 重點


if __name__ == '__main__':
    added_thread_example()
# Thread StartNext Code

# execute job0
# execute job1
# execute job2
# execute job3
# execute job4
# execute job5
# execute job6
# execute job7
# execute job8
# execute job9
# execute job10
# execute job11
# execute job12
# execute job13
# execute job14
# execute job15
# execute job16
# execute job17
# execute job18
# execute job19
# Thread Finish
```

**補充： 兩個執行緒一起執行的狀況 這邊我把第一條執行緒.join 放在執行 print(“Next Code”)前執行完畢，由於第二條執行緒執行的工作少於第一條執行緒，所以會在執行完第一條執行緒前執行完畢 實驗：大家可以根據自己的調整.join 的位置**

```python
## 導入套件
import threading
import time

def added_thread_job():
    print("Thread Start")

    ## 執行工作， 工作內容要執行20次，每次要執行0.1秒，來將執行工作時間拉長
    for i in range(20):
        time.sleep(0.1)
        print('execute job' + str(i))

    print('Thread Finish')

def added_thread_example():
    ## 新建執行緒
    added_thread = threading.Thread(target = added_thread_job, name = 'new_added_thread')

    ## 執行執行緒
    added_thread.start()

    ## 等到此執行緒執行完
    added_thread.join()# !重點

    print('Next Code')


if __name__ == '__main__':
    added_thread_example()

# Thread Start
# execute job0
# execute job1
# execute job2
# execute job3
# execute job4
# execute job5
# execute job6
# execute job7
# execute job8
# execute job9
# execute job10
# execute job11
# execute job12
# execute job13
# execute job14
# execute job15
# execute job16
# execute job17
# execute job18
# execute job19
# Thread Finish
# Next Code
```

- 先後更為明顯

```python
## 導入套件
import threading
import time

## 第一條執行緒執行的工作
def added_thread_job1():
    print("Thread 1 Start")

    ## 執行工作， 工作內容要執行5次，每次要執行0.1秒，來將執行工作時間拉長
    for i in range(5):
        time.sleep(0.1)
        print('execute job' + str(i)+'是1')

    print('Thread 1 Finish')

## 第二條執行緒執行的工作
def added_thread_job2():
    print("Thread 2 Start")

    ## 執行工作， 工作內容要執行2次，每次要執行0.1秒，來將執行工作時間拉長
    for i in range(2):
        time.sleep(0.1)
        print('execute job' + str(i)+'是2')

    print('Thread 2 Finish')



def added_thread_example():
    ## 新建執行緒
    added_thread1 = threading.Thread(target = added_thread_job1, name = 'new_added_thread1')
    added_thread2 = threading.Thread(target = added_thread_job2, name = 'new_added_thread2')


    ## 執行第一條執行緒
    added_thread1.start()

    ## 執行第二條執行緒
    added_thread2.start()

    ## 等到第一條執行緒執行完
    added_thread1.join()

    ## 等到第二條執行緒執行完
    added_thread2.join()

    print('Next Code')

if __name__ == '__main__':
    added_thread_example()
# Thread 1 Start
# Thread 2 Start
# execute job0是1
# execute job0是2
# execute job1是1
# execute job1是2
# Thread 2 Finish
# execute job2是1
# execute job3是1
# execute job4是1
# Thread 1 Finish
# Next Code
```

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### Queue 佇列

- 說明: 用來儲存多執行緒的個別運算結果，最後再從 Queue 中取得最終結果
- 重要: 由於多執行緒(或稱多線程)，不能像平常那樣使用 return 來回傳函數(function)結果，所以需要用到 Queue 的方式來取得函數(function)的結果
  > 首先: 我們需要導入 Queue 的套件: from queue import Queue
  > 再來: q.put()來回傳函數(function)結果到 Queue 中，與 return 的意思是一樣的
  > 最後: q.get()按順序從序列中取得結果值，一次只取一個值

```python
## 導入套件
import threading
import time
## 導入Queue所需的套件
from queue import Queue

## 定義執行緒欲直行的函數(工作)
def thread_job(l,q):
    ## 將資料集做平方運算
    for i in range(len(l)):
        l[i] = l[i]**2

    ## 回傳值: 回傳到Queue中
    q.put(l)

## 定義多執行緒的函數
def multi_threading():
    ## 啟用Queue佇列
    q = Queue()

    ## 用來裝所有創建的執行緒
    threads = []

    ## 自行定義的數據集
    data = [[2,4,8],[2,6,10],[3,7,9],[8,9,3],[5,5,6]]

    ## 定義五個執行緒，並放入threads裡
    for d in range(5):

        ## 定義執行緒
        t = threading.Thread(target = thread_job, args = (data[d], q))

        ## 啟用執行緒
        t.start()

        ## 放入threads裡
        threads.append(t)


    ## 使用.join()將五個執行緒家道主執行緒之中，並確保它們執行完畢，才進行下一步
    for thread in threads:
        thread.join()


    ## 創建一個串列(list)來裝載結果
    results = []

    ## 將Queue中的結果取回
    for r in range(5):
        results.append(q.get())

    print(results)


if __name__ == '__main__':
    multi_threading()
# [[4, 16, 64], [4, 36, 100], [9, 49, 81], [64, 81, 9], [25, 25, 36]]
```

- 如果資料匯入的執行緒太多，也有可能導致電腦 crash。
- 使用 ThreadPoolExecutor（內建限制數量）

```python
from concurrent.futures import ThreadPoolExecutor

def thread_job(l):
    return [i**2 for i in l]

def safe_multi_threading():
    data = [[2,4,8],[2,6,10],[3,7,9],[8,9,3],[5,5,6]]
    results = []

    # 最多同時執行 2 個執行緒
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(thread_job, d) for d in data]
        for future in futures:
            results.append(future.result())

    print(results)

if __name__ == '__main__':
    safe_multi_threading()
```

- 方法 2：限制資料分批處理，假設你有 1,000 筆資料，就用批次方式分批送入執行緒，例如每次 50 筆。

- 方法 3：監控記憶體和 CPU 使用率，你可以用工具（如 Windows 的工作管理員、Linux 的 top 或 htop）來觀察程式執行時的記憶體／CPU 使用情況。

- 如果你要處理大量資料，可以考慮使用：
  - ThreadPoolExecutor
  - multiprocessing（真正用多核心，適合 CPU 密集）
  - asyncio（I/O 密集）

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### GIL(Global Interpreter Lock)

- 前面有提到受到 GIL(Global Interpreter Lock )限制，Python 的多執行緒（Multi-Threading）執行速度並沒有比較快，這邊我們來測試一下是否是真的

```python
## 導入套件
import threading
import time
import copy
## 導入Queue所需的套件
from queue import Queue

## 多執行緒欲直行的函數(工作)
def thread_job(l,q):
    ## 計算數據串列中的總和
    total = sum(l)

    ## 回傳結果
    q.put(total)


## 定義多執行緒的函數
def multi_threading(l):
    ## 啟用Queue佇列
    q = Queue()
    ## 用來裝執行緒
    threads = []

    ## 定義五個執行緒，並放入threads裡
    for d in range(5):
        ## 定義執行緒
        t = threading.Thread(target = thread_job, args = (copy.copy(l), q), name = 'Thread %d' % d)

        ## 啟用執行緒
        t.start()

        ## 放入threads裡
        threads.append(t)


    ## 使用.join()將這五個執行緒加到主執行緒之中，並確保它們都有執行完畢，才進行下一步
    for thread in threads:
        thread.join()

    ## 創建一個串列(list)來裝結果
    results = []

    ## 將Queue中的運算結果取回
    for r in range(5):
        results.append(q.get())


    print('Multi Threading Method: ', results[0])


## 定義不使用Multi-Threading的函數
def normal_method(l):
    total = sum(l)
    print('Normal Method: ', total)


if __name__ == '__main__':
    ## 創建一組數據串列
    l = list(range(1000000))

    ## 記下當下的時間
    c_t = time.time()


    ## 執行一般運算的方法
    normal_method(l*5)

    ## 紀錄執行時間
    nt = time.time() - c_t

    ## 印出一般的執行時間
    print('Normal Time: ', nt)

    ## 記下當下時間
    c_t1 = time.time()

    ## 執行Multi-Threading運算
    multi_threading(l)

    ## 紀錄執行的時間
    mt = time.time() - c_t1

    ## 印出Multi Threading的執行時間
    print('Multi-Threading: ', mt)

    ## 一般與多執行緒的執行時間差
    print('Normal Time - Multi-Threading: ', nt - mt)
# Normal Method:  2499997500000
# Normal Time:  0.1399996280670166
# Multi Threading Method:  499999500000
# Multi-Threading:  0.16934800148010254
# Normal Time - Multi-Threading:  -0.029348373413085938
```

- 為什麼 normal_method(l\*5)要把數據乘以 5 說明： 因為我們使用五個執行緒同時執行同一筆數據，就等同於一般狀況下做五次，所以要乘 5，才能比較運算速度喔
- 結果： 理論來說，我們使用五個執行緒來執行，所運算的時間應該要只有一般狀況下的 1/5，但從執行結果來看，Multi-Threading 在速度上並沒有比一般快，或只有快一點點

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### Lock 鎖住

- 使用時機在使用多執行緒(Multi-Threading)時，每個執行緒都會同時執行，但有時候我們不能讓多個執行緒同時執行，像是我們不希望同時寫入檔案，這樣可能會造成錯亂，簡單來說就是我們希望執行緒等待上一個執行緒完成工作後，才能進行工作，一次只允許一個執行緒執行工作，這時我們就會使用 lock
- 兩個重要的 lock 使用方法

  > i. Lock.acquire: 當執行緒使用 acquire 時，就會獲得執行的權利，這時候只有它能夠執行，其他執行緒要等它執行完畢，才能執行
  > ii. Lock.release: 當執行緒使用 release，就會釋放執行的權利，讓下一個呼叫 acquire 的執行緒獲取執行權利

- 防止被干擾，要完成第一個才可以下一個，避免交錯。

```python
## 導入套件
import threading
import time

## 定義兩個函數(工作) 分別由兩個執行緒來執行
def thread_job1():
    ## 將result 定義為全域變數
    global result

    ## 執行20次，每次將result值加1
    for i in range(20):
        result += 1
        print("thread job1: ", result)


def thread_job2():
    ## 將result 定義為全域變數
    global result

    ## 執行20次，每次將result值加1
    for i in range(20):
        result += 2
        print("thread job2: ", result)

if __name__ == '__main__':
    result = 0

    ## 定義兩條執行緒，分別執行兩種函數(工作)
    thread1 = threading.Thread(target = thread_job1)#, name = 'new_added_thread1')
    thread2 = threading.Thread(target = thread_job2)#, name = 'new_added_thread2')


    ## 執行
    thread1.start()
    thread2.start()

    ## 執行完畢
    thread1.join()
    thread2.join()
# thread job1:  1
# thread job1:  2
# thread job1:  3
# thread job1:  4
# thread job1:  5
# thread job1:  6
# thread job1:  7
# thread job1:  thread job2:  10
# 8
# thread job1:  11
# thread job1:  12
# thread job1:  13thread job2:  15
# thread job2:  17
# thread job2:  19
# thread job2:
# thread job1:  22
# thread job1:  23
# thread job1:  24
# thread job1:  25
# thread job1:  26
# thread job1:  27
# thread job1:  28
# thread job1:  29
# thread job1:  30
# 21
# thread job2:  32
# thread job2:  34
# thread job2:  36
# thread job2:  38
# thread job2:  40
# thread job2:  42
# thread job2:  44
# thread job2:  46
# thread job2:  48
# thread job2:  50
# thread job2:  52
# thread job2:  54
# thread job2:  56
# thread job2:  58
# thread job2:  60

## 導入套件
import threading
​
## 定義兩個函數(工作) 分別由兩個執行緒來執行
def thread_job1():
    ## 將lock、result定義為全域變數
    global lock, result

    ## 獲取執行權
    lock.acquire()

    ## 執行20次，每次將result值加1
    for i in range(20):
        result += 1
        print("thread job1: ", result)

    ## 釋放執行權
    lock.release()


def thread_job2():
    ## 將locl、result定義為全域函數
    global lock, result

    ## 獲取執行權
    lock.acquire()

    ## 執行20次，每次將result值加2
    for i in range(20):
        result +=2
        print("thread job2: ", result)

    ## 釋放執行權
    lock.release()


if __name__ == '__main__':

    ## 定義lock的方法
    lock = threading.Lock()

    result = 0

    ## 定義兩條執行緒，分別執行兩種函數(工作)
    thread1 = threading.Thread(target = thread_job1)
    thread2 = threading.Thread(target = thread_job2)

    ## 執行
    thread1.start()
    thread2.start()


    ## 執行完畢
    thread1.join()
    thread2.join()
# thread job1:  1
# thread job1:  2
# thread job1:  3
# thread job1:  4
# thread job1:  5
# thread job1:  6
# thread job1:  7
# thread job1:  8
# thread job1:  9
# thread job1:  10
# thread job1:  11
# thread job1:  12
# thread job1:  13
# thread job1:  14
# thread job1:  15
# thread job1:  16
# thread job1:  17
# thread job1:  18
# thread job1:  19
# thread job1:  20
# thread job2:  22
# thread job2:  24
# thread job2:  26
# thread job2:  28
# thread job2:  30
# thread job2:  32
# thread job2:  34
# thread job2:  36
# thread job2:  38
# thread job2:  40
# thread job2:  42
# thread job2:  44
# thread job2:  46
# thread job2:  48
# thread job2:  50
# thread job2:  52
# thread job2:  54
# thread job2:  56
# thread job2:  58
# thread job2:  60
```

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### Semaphore 旗標

- 說明： 功能類似於 Lock，但 Lock 一次只允許一個執行緒進行工作，而 Semaphore 允許多個執行緒同時工作，但要限制數量，它也是用 acquire 來獲取執行權，release 來釋放執行權，但不同的是 Semaphore 在執行這兩個函數時，多了一個計數器的概念，當 acquire 時會-1，release 時會+1，減到為 0 時，下一個執行緒就需要正在執行工作執行緒 release 釋放權限後，才能執行
- 使用時機： 因為系統的資源有限，像是 CPU 或記憶體限制，在執行很耗資源的程式時，我們希望限制同時執行工作的執行緒數量，才不會造成系統執行很慢
- 使用方法： threading.Semaphore()函數裡面的參數為限制同時執行的執行緒數量，像是 threading.Semaphore(2)，代表同時限制兩個執行緒執

```python
import threading
import time

# 最多允許 2 個執行緒同時執行
semaphore = threading.Semaphore(2)

def task(thread_id):
    print(f"執行緒 {thread_id} 嘗試取得旗標...")

    with semaphore:  # acquire + 自動 release
        print(f"✅ 執行緒 {thread_id} 已取得旗標，開始執行")

        time.sleep(2)  # 模擬耗時任務
        print(f"⏹️ 執行緒 {thread_id} 執行完畢，釋放旗標")

    print(f"🔓 執行緒 {thread_id} 離開臨界區")

# 建立多個執行緒（5個）
threads = []
for i in range(5):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

# 等待所有執行緒完成
for t in threads:
    t.join()

# 執行緒 0 嘗試取得旗標...
# ✅ 執行緒 0 已取得旗標，開始執行
# 執行緒 1 嘗試取得旗標...
# ✅ 執行緒 1 已取得旗標，開始執行
# 執行緒 2 嘗試取得旗標...
# 執行緒 3 嘗試取得旗標...
# 執行緒 4 嘗試取得旗標...
# ⏹️ 執行緒 0 執行完畢，釋放旗標
# 🔓 執行緒 0 離開臨界區
# ✅ 執行緒 2 已取得旗標，開始執行
# ⏹️ 執行緒 1 執行完畢，釋放旗標
# 🔓 執行緒 1 離開臨界區
# ✅ 執行緒 3 已取得旗標，開始執行
# ⏹️ 執行緒 2 執行完畢，釋放旗標
# 🔓 執行緒 2 離開臨界區
# ✅ 執行緒 4 已取得旗標，開始執行
# ⏹️ 執行緒 3 執行完畢，釋放旗標
# 🔓 執行緒 3 離開臨界區
# ⏹️ 執行緒 4 執行完畢，釋放旗標
# 🔓 執行緒 4 離開臨界區
```

$\blue\bigstar$ [執行面 (實例)](#執行面-實例)

### RLock

- 說明： 為一個可以重複取得執行權的方法，與 Lock 功能類似，但是它可以允許同一個執行緒，重複取得執行的權利，RLock 也有計數器的概念，但與 Semaphore 不同的點在於 acquire 獲取權限的時候會+1，release 釋放權限時會-1，剛好與 Semaphore 相反，當遞減到 0 時，才會真的釋放執行權，大於 0 的時候，其它執行緒都不能獲得執行權

```python
## 啟動RLock
rlock = threading.RLock()
​
## 取得執行權
rlock.acquire()
​
## 重複取得執行權，不會被擋住
rlock.acquire()
​
## 釋放執行權
rlock.release
​
## 再次釋放執行權
rlock.release()
```

```python
import threading
import time

lock = threading.RLock()

def job_with_rlock():
    print(f"[{threading.current_thread().name}] 嘗試第一次取得 RLock")

    lock.acquire()
    print(f"[{threading.current_thread().name}] 已取得 RLock 第一次")
    # 再次進入同一鎖（可重入）
    print(f"[{threading.current_thread().name}] 嘗試第二次取得 RLock")

    lock.acquire()
    print(f"[{threading.current_thread().name}] 已取得 RLock 第二次")

    print(f"[{threading.current_thread().name}] 執行中...")
    time.sleep(1)

    # 釋放兩次，對應兩次 acquire
    lock.release()
    print(f"[{threading.current_thread().name}] 已釋放一次 RLock")
    lock.release()
    print(f"[{threading.current_thread().name}] 已釋放第二次 RLock")

# 建立執行緒
t1 = threading.Thread(target=job_with_rlock, name="Thread-1")
t2 = threading.Thread(target=job_with_rlock, name="Thread-2")

t1.start()
t2.start()

t1.join()
t2.join()

# [Thread-1] 嘗試第一次取得 RLock
# [Thread-1] 已取得 RLock 第一次
# [Thread-1] 嘗試第二次取得 RLock
# [Thread-1] 已取得 RLock 第二次
# [Thread-1] 執行中...
# [Thread-2] 嘗試第一次取得 RLock
# [Thread-1] 已釋放一次 RLock
# [Thread-1] 已釋放第二次 RLock
# [Thread-2] 已取得 RLock 第一次
# [Thread-2] 嘗試第二次取得 RLock
# [Thread-2] 已取得 RLock 第二次
# [Thread-2] 執行中...
# [Thread-2] 已釋放一次 RLock
# [Thread-2] 已釋放第二次 RLock
```

$\blue\bigstar$ [回到表目錄](#Threading)

## 執行面(注意的反例)

### Solution 1 方案 1 - 標準單一執行緒解法 - 慢但是穩健不會有錯誤

```python
# 使用標準非執行緒的作法
NUM_ITER = 100
counter = 0
sum_ = 0


def do_work():
    global counter
    global sum_

    counter = counter + 1
    next_sum = sum_ + counter
    print(f"{sum_} + {counter} = {next_sum}")
    print("-" * 20)
    sum_ = next_sum


for i in range(NUM_ITER):
    do_work()

print(f"DONE: solution = {sum_}")
```

### Solution 2 方案 2 - 標準多執行緒作法，但忽略了執行緒中是否所有函式都為 Thread-Safe 問題

- 執行此程式幾次，很快就會發現有遇到了一些狀況。
- 第一個注意到的狀況是， ---- 程式碼列並非總是出在正確的位置。
- 這是由於 print 不是安全的執行緒
  - print 實際上會緩衝其輸出，而此處的輸出會在所有執行緒之間共用
  - 因而有共用資源 (主控台或 stdout )，而寫入該輸出可能會被另一個執行緒中斷，進而導致此狀況。此種由多個執行緒競爭搶佔共用資源的狀況稱為競爭條件。

```python
import threading

NUM_ITER = 100
counter = 0
sum_ = 0


def do_work():
    global counter
    global sum_

    counter += 1
    next_sum = sum_ + counter
    print(f"{sum_} + {counter} = {next_sum}")
    print("-" * 20)
    sum_ = next_sum


threads = []

# create the threads
for i in range(NUM_ITER):
    threads.append(threading.Thread(target=do_work))

# start the threads
for thread in threads:
    thread.start()

# wait until all threads are done
for thread in threads:
    thread.join()

print(f"DONE: solution = {sum_}")
```

### Solution 3 解決方案 3 - 使用 Thread Lock 來解決 Print() 非 thread-safe 引發的問題

- 當我們使用程序鎖定時，我們需要確保在程式碼中的每個地方都自行放置這些程序鎖定 - 程序鎖定的運作方式是，我們建立或取得程序鎖定，執行一些工作，然後釋放程序鎖定，「執行緒 2，你必須等到執行緒 1 釋放其程序鎖定才能繼續並取得程序鎖定」
- 似乎我們已經解決了我們的列印問題，然而我們的計算完全錯誤

```python
import threading


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()


def do_work():
    global counter
    global sum_

    counter += 1
    next_sum = sum_ + counter
    p_lock.acquire()
    print(f"{sum_} + {counter} = {next_sum}")
    print("-" * 20)
    p_lock.release()
    sum_ = next_sum


threads = []

# create the threads
for i in range(NUM_ITER):
    threads.append(threading.Thread(target=do_work))

# start the threads
for thread in threads:
    thread.start()

# wait until all threads are done
for thread in threads:
    thread.join()

print(f"DONE: solution = {sum_}")
```

### Solution 3a 解法 3a - 解決程序鎖定的例外導致的問題

- 程序鎖定物件其實也實作了內容管理員物件，因此我們可以簡單地使用內容管理員，而不必自己撰寫 acquire() 和 release() ，這讓程序鎖定變得簡單多了，它讓我們不必處理可能發生在 acquire() 和 release() 之間的例外狀況（而且可能無法釋放程序鎖定）。

```python
import threading


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()


def do_work():
    global counter
    global sum_

    counter += 1
    next_sum = sum_ + counter
    with p_lock:
        print(f"{sum_} + {counter} = {next_sum}")
        print("-" * 20)
    sum_ = next_sum


threads = []

# create the threads
for i in range(100):
    threads.append(threading.Thread(target=do_work))

# start the threads
for thread in threads:
    thread.start()

# wait until all threads are done
for thread in threads:
    thread.join()

print(f"DONE: solution = {sum_}")
```

### Solution 4 解決方案 4 - 在 Print function 以外的地方加入防止搶佔的程序鎖定

- 請記住，執行緒可能會在任何時間中斷，且大多數的情況下將超出我們的控制（這就是所謂的搶佔式多工處理）
- 如果我們執行這幾次，看起來我們得到了正確的最終結果（ 5050 ），但如果我們執行程式幾次，並仔細觀察，中間結果似乎並不完全正確。
- 雖然我們消除了競爭條件，但我們仍然有一個問題，即執行緒沒有按照正確的順序執行計算（因為我們無法控制執行緒何時執行和中斷）。
  - 至少我們得到了正確的最終結果。但中間計算顯示是錯誤的。

```python
import threading


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()
c_lock = threading.Lock()


def do_work():
    global counter
    global sum_

    with c_lock:
        prev_sum = sum_
        counter += 1
        next_sum = sum_ + counter
        sum_ = next_sum

    with p_lock:
        print(f"{prev_sum} + {counter} = {next_sum}")
        print("-" * 20)


threads = []

# create the threads
for i in range(NUM_ITER):
    threads.append(threading.Thread(target=do_work))

# start the threads
for thread in threads:
    thread.start()

# wait until all threads are done
for thread in threads:
    thread.join()

print(f"DONE: solution = {sum_}")
```

### Solution 5 解決方案 5 - 使用 fuzzing 技術幫每個執行緒加入任意的延遲以確保每個程序能夠完整走完

- 我們將通過在 do_work 函數的執行時間中引入一些可變性來加劇我們在最後一個解決方案中看到的問題。
- 這不是我們可以用程序鎖定解決的問題。我們需要確保以某種方式按順序執行正在執行的作業，而這通常不是並行程式設計的運作方式
- 並行程式設計的一個關鍵原則是執行順序不是重要，對於所獲得的最終結果，我們的演算法似乎運作良好，然而中間計算過程的顯示則完全錯誤。

```python
import random
import threading
from time import sleep


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()
c_lock = threading.Lock()


def fuzz():
    sleep(random.random() / 10)


def do_work():
    global counter
    global sum_

    fuzz()
    with c_lock:
        counter += 1
        curr_counter = counter
        prev_sum = sum_
        next_sum = sum_ + counter
        sum_ = next_sum
    fuzz()
    with p_lock:
        print(f"{prev_sum} + {curr_counter} = {next_sum}")
        print("-" * 20)
    fuzz()


threads = []

# create the threads
for i in range(NUM_ITER):
    threads.append(threading.Thread(target=do_work))

# start the threads
for thread in threads:
    thread.start()

# wait until all threads are done
for thread in threads:
    thread.join()

print(f"DONE: solution = {sum_}")
```

### Solution 6 方案 6 - 改用佇列來解決未按照順序列印的計算過程顯示問題

- 我個人認為這之所以有效的原因是，我們基本上將鎖定放在整組計算上
- 這基本上會阻止任何其他執行緒中斷計算，本質上使我們的計算流程「線性」而不是真正並行。

```python
import queue
import random
import threading
from time import sleep


NUM_ITER = 100
counter = 0
sum_ = 0
c_lock = threading.Lock()
print_queue = queue.Queue()


def fuzz():
    sleep(random.random() / 10)


def print_queue_watcher():
    while True:
        item = print_queue.get()
        fuzz()
        print(item)
        fuzz()
        print_queue.task_done()
        fuzz()


def do_work():
    global counter
    global sum_

    fuzz()
    with c_lock:
        counter += 1
        next_sum = sum_ + counter
        print_queue.put(f"{sum_} + {counter} = {next_sum}")
        print_queue.put("-" * 20)
        sum_ = next_sum
    fuzz()


threads = []

# start daemon print watcher thread
threading.Thread(target=print_queue_watcher, daemon=True).start()

# create the threads
for i in range(NUM_ITER):
    threads.append(threading.Thread(target=do_work))

# start the threads with some fuzzing between starts
for thread in threads:
    thread.start()
    fuzz()

# wait until all threads are done
for thread in threads:
    thread.join()

# wait until the print queue is empty
print_queue.join()

print(f"DONE: solution = {sum_}")
```

$\blue\bigstar$ [回到表目錄](#Threading)

## 資料庫

- Python 的 threading 模組特別適用於 I/O-bound 工作，像是：
  - 網路爬蟲（等待網頁回應）
  - 檔案讀寫
  - 資料庫操作
  - 等待硬碟、網路、API 等外部設備
  - 這些工作本身不會吃太多 CPU，但會讓主程式「卡住等待」，這時用多執行緒可以「一邊等，一邊做別的事情」，大幅減少總時間。
- 避免記憶體 Crash？不是主要目的，但有關係 - 多執行緒本身並不會特別節省記憶體，反而會因為多個執行緒同時存在： - 佔用更多記憶體（每個 thread 有自己的堆疊） - 若沒管控好，可能會導致資源爭奪、死鎖、記憶體問題
  > 🧯 但你提到「避免記憶體 crash」這件事，是在有大量任務或不當同步時，有些人會 **使用多執行緒 + 限流 像是 Semaphore**來避免開太多資源導致崩潰，這是控制風險，不是本質目的。

| 目的                   | 是否主要目的 | 補充說明                                 |
| ---------------------- | ------------ | ---------------------------------------- |
| ✅ 節省總執行時間      | ✅ 是        | 特別對 I/O-bound 任務                    |
| ⚠️ 資源分配避免 crash  | ❌ 否        | 不是本意，但多執行緒可搭配控制機制來避免 |
| ❌ 加速 CPU-heavy 工作 | ❌ 否        | 應該用多處理程序（`multiprocessing`）    |

- 資料庫操作本質屬於 I/O-bound - 資料庫查詢（例如 MySQL、PostgreSQL、MongoDB 等）需要： - 對資料庫伺服器發出請求（透過網路或本地連接） - 等待資料庫執行查詢（耗時） - 等待回傳結果（又是等待）

  > ⚠️ 這中間可能花 10ms ~ 幾秒，執行緒大部分時間是 在等，不是在用 CPU。

- 使用多執行緒的時機 - 同時查多張表、多筆資料 - 一邊查資料，一邊處理前面的資料 - 做 ETL（Extract-Transform-Load）流程時，有大量讀寫
  > 用單執行緒查詢資料 → 你只能等一筆查完再查下一筆。
  > 但如果你用多執行緒（或多協程）→ 可以同時發出多個查詢請求，不浪費等待時間。

📘 實務案例 1：爬蟲後存資料到資料庫

```python
def save_to_db(data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (data['title'], data['content']))
    conn.commit()
    conn.close()
```

> 如果你有上千筆資料需要存，就可以：每筆資料用一個 thread 或用 ThreadPoolExecutor、避免存資料變成瓶頸

📘 實務案例 2：報表系統多筆 SQL 查詢

- 你有一個 Dashboard 要查：

  - 公司數量;使用者總數
  - 訂單總額
  - 聯盟;各地區活躍度

- 採用單緒

```python
# 三次分開查詢
q1 = query_users()
q2 = query_orders()
q3 = query_regions()
```

- 採用多緒執行

```python
with ThreadPoolExecutor() as executor:
    f1 = executor.submit(query_users)
    f2 = executor.submit(query_orders)
    f3 = executor.submit(query_regions)

    q1 = f1.result()
    q2 = f2.result()
    q3 = f3.result()
```

⚠️ 多執行緒操作資料庫的注意事項

| 問題                          | 說明                                                                      |
| ----------------------------- | ------------------------------------------------------------------------- |
| ❌ 資料庫連線不是 thread-safe | 某些資料庫（像 SQLite）不支援多執行緒共享連線，要每個 thread 用自己的連線 |
| ❗ 避免太多同時查詢           | 如果你開 1000 thread 同時查，DB 會 overload                               |
| ✅ 可以用 Connection Pool     | 建議搭配像 `SQLAlchemy` 的 connection pool 控管                           |

🛠️ 什麼情境適合多執行緒資料庫操作？

| 情境             | 是否適合                             |
| ---------------- | ------------------------------------ |
| 查很多使用者資訊 | ✅ 非常適合                          |
| 大量資料批次寫入 | ✅ 適合，但要控管                    |
| 即時報表查詢     | ✅ 適合（提升回應速度）              |
| 複雜 join 查詢   | ❌ 不適合（應優化 SQL 或資料表結構） |

🔚 結論

多執行緒在資料庫操作中，主要是用來提升「查詢/寫入效率」，尤其對於 I/O-bound、非阻塞性的資料需求 來說，可以大幅縮短總耗時。

> 同時查 100 筆使用者資訊
> 多執行緒匯入 CSV 到資料庫
> 多查詢比單查詢快幾秒的實驗

| 使用情境     | max_workers | pool_size 建議 | 說明                       |
| ------------ | ----------- | -------------- | -------------------------- |
| 小量平行查詢 | 4\~8        | 6\~10          | 預設建議配置，安全穩定     |
| 中量查詢     | 10\~20      | 12\~24         | 批次任務或多板查詢時       |
| 大量 ETL     | 20+         | 25\~40         | 嚴格控制錯誤處理與資源管理 |

ETL（Extract, Transform, Load，提取、轉換、載入） 的完整介紹

1. 資料擷取（Extract）

- 功能：
  - 從各種來源系統擷取資料，例如：
  - 關聯式資料庫（如 Oracle、SQL Server、MySQL）
  - 非關聯式資料庫（如 MongoDB、Cassandra）
  - 應用程式介面（API）
  - CSV、JSON、XML、Excel 等檔案格式
  - 主機系統或舊有系統
  - 第三方平台（如 Salesforce、Google Analytics）
- 注意事項：
  - 資料編碼處理（如 BIG5 → UTF-8）
  - 欄位重命名與資料格式處理（如時間格式統一）
  - 資料品質初檢（欄位是否遺失、格式是否正確）
  - 儲存原始資料以利追蹤與備查
  - 容錯與擷取策略（例如增量擷取、全量擷取）

2. 資料轉換（Transform）

- 功能：
  - 將擷取到的原始資料依照目標格式或邏輯進行清洗與轉換。
  - 欄位重命名與資料格式處理（如時間格式統一）
  - 代碼轉換（例如國碼、幣別單位）
  - 資料彙整、分群、排序、聚合
  - 立維度表（Dim）與事實表（Fact）以支援 BI 工具分析

| 類別                   | 說明                                               |
| ---------------------- | -------------------------------------------------- |
| **欄位轉換**           | 將欄位格式進行標準化（如日期、字串處理）           |
| **資料清理**           | 去除空值、重複值、異常值                           |
| **欄位合併或拆分**     | 例如將姓名拆為姓與名，或將地址欄位合併             |
| **代碼轉換**           | 例如民國年 → 西元年、地區代碼轉換                  |
| **業務邏輯應用**       | 根據條件產生分類、計算指標等                       |
| **參照查詢**           | 使用主資料表補齊欄位資料（如用戶 ID 查出用戶名稱） |
| **流水號、預設值處理** | 產生唯一識別碼或補上預設值                         |

- 轉換的挑戰：
  - 多資料源整併（欄位定義不一致）
  - 不同格式轉換（如 Excel → JSON）
  - 欄位邏輯複雜（依據業務規則選擇來源）
- 這些轉換作業常透過：
  - SQL 腳本
  - 資料倉儲提供的工作流程排程器
  - Airflow、DBT（Data Build Tool）等工具

| 工具                                                | 功能重點                                         |
| --------------------------------------------------- | ------------------------------------------------ |
| **Fivetran**                                        | 自動從多種資料源擷取並載入至倉儲，幾乎不需寫程式 |
| **Airbyte**                                         | 開源 ELT 工具，擴充性高，可自訂 connector        |
| **DBT (Data Build Tool)**                           | 專門針對資料倉儲進行 SQL 轉換與模型建構          |
| **Matillion**                                       | 可視化 ELT 平台，支援雲端資料倉儲                |
| **Google Dataflow / AWS Glue / Azure Data Factory** | 雲端平台整合資料流與轉換任務                     |

3. 資料載入（Load）

- 功能：
  - 將轉換好的資料寫入目標資料庫或資料倉儲中。
  - 大量資料並行寫入（支援批次與串流）
  - 原始資料保留以便日後比對或回朔
- 載入方式：
  - 全量載入：每次都覆蓋所有資料（適合開發階段）
  - 增量載入：只更新有異動的資料（適合正式環境）
  - 批次處理或即時處理：根據頻率或觸發事件處理載入
- 注意事項：
  - 預留轉換後資料快照以供比對
  - 載入順序與資料表關聯性需正確
  - 必須驗證資料筆數與內容正確性
  - 轉換紀錄（Log）需完整保留

資料移轉計畫七步驟（延伸自 ETL 專案）

- 制定移轉計畫

  > 評估整體移轉需求與時間、人力資源，制定明確時程。

- 計畫啟動

  > 確認跨部門共識，分配資源與角色。

- 範圍分析

  > 盤點來源與目的系統欄位、關聯性、缺失資料補齊方式。

- 解決方案設計

  > 包括欄位對應表、轉換邏輯、驗證策略。

- 構建與測試

  > 開發 ETL 流程或使用工具建置流程，進行測試與錯誤 Log 記錄。

- 執行並驗證

  > 正式轉換資料，並驗證筆數、資料一致性、內容正確性。

- 退役與監控
  > 舊系統關閉或設限讀取權限，對新資料持續監控與追蹤。

| 工具                                                 | 特點                                              |
| ---------------------------------------------------- | ------------------------------------------------- |
| **Informatica**                                      | 功能強大、企業級、支援複雜流程                    |
| **Talend**                                           | 開源、可自訂程式邏輯                              |
| **Microsoft SSIS (SQL Server Integration Services)** | 微軟生態系統中最常用的 ETL 工具                   |
| **Apache NiFi**                                      | 可視化資料流、適合即時資料處理                    |
| **Pentaho Data Integration (PDI)**                   | 支援批次與即時資料整合                            |
| **DataStage (IBM)**                                  | 大型企業多使用，整合性佳                          |
| **Airbyte / Fivetran**                               | 現代 SaaS 化 ETL 工具，支援大量資料源、無需寫程式 |

| 項目         | **ETL**                          | **ELT**                                        |
| ------------ | -------------------------------- | ---------------------------------------------- |
| 處理順序     | 提取 → 轉換 → 載入               | 提取 → 載入 → 轉換                             |
| 轉換位置     | 在外部伺服器或 ETL 工具中        | 在資料倉儲中                                   |
| 資料倉儲角色 | 儲存「轉換後」資料               | 儲存原始資料與轉換後資料                       |
| 性能依賴     | 依賴 ETL 工具處理能力            | 依賴資料倉儲（如 BigQuery、Snowflake）處理能力 |
| 適用場景     | 資料清理嚴謹、來源複雜、系統較舊 | 大數據、高並行處理、雲端環境                   |
| 運算資源     | 外部伺服器                       | 雲端倉儲（SQL 引擎、大數據引擎）               |
| 儲存需求     | 較小，因只存處理後資料           | 較大，會存下所有原始資料                       |

$\blue\bigstar$ [回到表目錄](#Threading)

## reference

- [可參考看-知識補充](https://chwang12341.medium.com/e233465f2084)
- [可參考看-知識補充](https://jianjiesun.medium.com/python%E7%AD%86%E8%A8%98-10-multi-thread-%E5%A4%9A%E5%9F%B7%E8%A1%8C%E7%B7%92-7eb54c6f59ed)
- [可參考看-知識補充](https://vocus.cc/article/65fbf77cfd897800014991a7)
- [偏不實用-知識補充](https://steam.oxxostudio.tw/category/python/library/threading.html)
- [crawl 1](https://www.maxlist.xyz/2020/03/15/python-threading/)
- [crawl 2](https://myapollo.com.tw/blog/python-threading-thread-pool/)
- [Code](https://colab.research.google.com/drive/18_kjWu5YODF4hVQShXs9z5S98v8bAlDl?pli=1&usp=sharing#scrollTo=uNwqk1kRFCH9)
