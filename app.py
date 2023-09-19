from argparse import Namespace
from email import message
from socket import socket
from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import random

from itsdangerous import NoneAlgorithm

###########################
#########CONFIG############
###########################

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = '5dec1cfe7c0c2ec55c17fb44b43f7d14'
socket_ = SocketIO(app, async_mode=async_mode)

insThread = None
ins_thread_lock = Lock()
selThread = None
sel_thread_lock = Lock()
qckThread = None
qck_thread_lock = Lock()
hepThread = None
hep_thread_lock = Lock()
radThread = None
rad_thread_lock = Lock()
bubbleThread = None
bubble_thread_lock = Lock()
mergeThread = None
merge_thread_lock = Lock()
bucketThread =None
bucket_thread_lock = Lock()

def insertion_sort(array, speed):
    global insThread       

    for step in range(1, len(array)):
        key = array[step]
        j = step  
        while j > 0 and array[j-1]>key:
            socket_.sleep(speed)
            socket_.emit('ins',{'data':{'algorithm':'insertion', 'array':array, 'step':step+1, 'compare':j}}, namespace='/sort')
            array[j] = array[j-1]
            j = j - 1
        array[j] = key
    socket_.sleep(speed)
    socket_.emit('ins',{'data':{'algorithm':'insertion', 'array':array, 'step':-1, 'compare':-1}}, namespace='/sort')
    insThread=None

def partition(array, low, high, speed):
  pivot = array[high]

  i = low - 1

  for j in range(low, high):
    socket_.emit('quick',{'data':{'algorithm':'quick', 'array':array}}, namespace='/sort')
    if array[j] <= pivot:
      i = i + 1
      socket_.emit('quick',{'data':{'algorithm':'quick', 'array':array}}, namespace='/sort')
      (array[i], array[j]) = (array[j], array[i])
    socket_.emit('quick',{'data':{'algorithm':'quick', 'array':array}}, namespace='/sort')

  (array[i + 1], array[high]) = (array[high], array[i + 1])
  socket_.sleep(speed)
  socket_.emit('quick',{'data':{'algorithm':'quick', 'array':array}}, namespace='/sort')

  return i + 1

def quickSort(array, low, high, speed):
  if low < high:
    pi = partition(array, low, high, speed)
    quickSort(array, low, pi - 1, speed)
    quickSort(array, pi + 1, high, speed)

def quick_sort(array, speed):
    global qckThread
    quickSort(array, 0, len(array)-1, speed)
    qckThread=None

def selection_sort(array, speed):
    global selThread

    for i in range(len(array)):
        bigindex=0
        for j in range(len(array)-i):
            socket_.sleep(speed)
            socket_.emit('sel',{'data':{'algorithm':'selection', 'array':array, 'step':bigindex, 'compare':j}}, namespace='/sort')
            if array[j]>array[bigindex]:
                bigindex=j
            
        array[bigindex], array[len(array)-i-1]=array[len(array)-i-1], array[bigindex]
        #socket_.sleep(speed)
        #socket_.emit('sel',{'data':{'algorithm':'selection', 'array':array, 'step':bigindex, 'compare':len(array)-i-1}}, namespace='/sort')
    socket_.sleep(speed)
    socket_.emit('sel',{'data':{'algorithm':'selection', 'array':array, 'step':-1, 'compare':-1}}, namespace='/sort')
    selThread=None

def heapify(arr, n, i, speed):
    # Find largest among root and children
      largest = i
      l = 2 * i + 1
      r = 2 * i + 2
  
      if l < n and arr[i] < arr[l]:
          largest = l
  
      if r < n and arr[largest] < arr[r]:
          largest = r

      # If root is not largest, swap with largest and continue heapifying
      if largest != i:
          arr[i], arr[largest] = arr[largest], arr[i]
          socket_.sleep(speed)
          socket_.emit('heap',{'data':{'algorithm':'heap', 'array':arr}}, namespace='/sort')
          heapify(arr, n, largest, speed)

def heap_sort(arr, speed):
      global hepThread
      n = len(arr)
  
      # Build max heap
      for i in range(n//2, -1, -1):
          socket_.emit('heap',{'data':{'algorithm':'heap', 'array':arr}}, namespace='/sort')
          heapify(arr, n, i, speed)
          socket_.emit('heap',{'data':{'algorithm':'heap', 'array':arr}}, namespace='/sort')
  
      for i in range(n-1, 0, -1):
          # Swap
          arr[i], arr[0] = arr[0], arr[i]
  
          # Heapify root element
          socket_.emit('heap',{'data':{'algorithm':'heap', 'array':arr}}, namespace='/sort')
          heapify(arr, i, 0, speed)
          socket_.emit('heap',{'data':{'algorithm':'heap', 'array':arr}}, namespace='/sort')
      hepThread=None

def radix_sort(nums, speed):
    global radThread
    RADIX=10
    placement=1
    max_digit=max(nums)
    while placement<max_digit:
        buckets=[list() for _ in range(RADIX)]
        tempArr={}
        for i in range(len(nums)):
            tempArr[i]=nums[i]
        for i in range(len(nums)):
            tmp=int((nums[i]/placement)%RADIX)
            arr=[j for j in tempArr.values()]
            for b in buckets:
                arr.extend(b)
            socket_.sleep(speed)
            socket_.emit('radix',{'data':{'algorithm':'radix', 'array':arr}}, namespace='/sort')
            buckets[tmp].append(nums[i])

            del tempArr[i]

        a=0
        for b in range(RADIX):
            buck=buckets[b]
            for i in buck:
                nums[a]=i
                a+=1
        placement*=RADIX
        socket_.emit('radix',{'data':{'algorithm':'radix', 'array':nums}}, namespace='/sort')
    radThread=None

def bubble_sort(array, speed):
    global bubbleThread
    num = len(array)
    for i in  range (0, num):
        for j in range (0, num-i-1):
            socket_.sleep(speed)
            socket_.emit('bub',{'data':{'algorithm':'BubbleSort', 'array':array, 'end': len(array)}}, namespace='/sort')
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

    bubbleThread = None

def merge(array, s, m, e, speed):
    left = array[s:m+1]
    right = array[m+1:e+1]

    count, recurce = 0, 0
    sorted = s
    socket_.sleep(speed)
    socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
    while count < len(left) and recurce < len(right):
        # sorting the left half of the array passsed
        socket_.sleep(speed)
        socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
        if left[count] <= right[recurce]:
            socket_.sleep(speed)
            socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
            array[sorted] = left[count]
            count+=1
        else:
            # sorting the right halfof array passed
            socket_.sleep(speed)
            socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
            array[sorted] = right[recurce]
            recurce += 1

        sorted += 1
    # Loop check if one half is sorted before the end of other half
    while count < len(left):
        socket_.sleep(speed)
        socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
        array[sorted] = left[count]
        count += 1
        sorted += 1
    # wait check if the right half is not sorted by the time left half has been sorted
    while recurce < len(right):
        socket_.sleep(speed)
        socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
        array[sorted] = right[recurce]
        recurce += 1
        sorted += 1
    socket_.sleep(speed)
    socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')

def merge_sort(array, start, end, speed):
    global mergeThread
    print ("Merge Sorts'Sorted Array: ", array)
    if start >= end:
        return
    
    mid = (start + end) // 2
    socket_.sleep(speed)
    socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
    
    merge_sort(array, start, mid, speed)

    merge_sort(array, mid+1, end, speed)
    
    socket_.sleep(speed)
    socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')

    
    
    merge(array, start, mid, end, speed)
    socket_.sleep(speed)
    socket_.emit('merge',{'data':{'algorithm':'mergesort', 'array':array}}, namespace='/sort')
    
   
    mergeThread = None

def bucket_insertion(element):
    for sorted in range(1, len(element)):
        insert = element[sorted]    # taking a sorted initial index
        j = sorted - 1
        while j >= 0 and element[j] > insert:   #checking if index is less then the sorted key
            element[j + 1] = element[j]         # swapping
            j -= 1                              # the
        element[j + 1] = insert                 # indexes
    return element   


def bucket_sort(array, speed):
    global bucketThread

    arr = []        # array for buckets
    bucket = 10     # declaring no.of buckets to store index elements
    for i in range(bucket):
        arr.append([])  # initializing the bucket array
          
    # Put array elements in different buckets 
    for j in array:
        in_bucket = int(bucket//10)     
        arr[in_bucket].append(j)    #appending the element of original array in buckets

    # Sort individual buckets 
    for i in range(bucket):
        # visualizing the elements being sorted through insertion sort
        socket_.sleep(speed)
        socket_.emit('buck',{'data':{'algorithm':'BucketSort', 'array':array}}, namespace='/sort')                      # making new figure on every sort swap
        arr[i] = bucket_insertion(arr[i])  # calling secondary sorting algorithm
        
    # concatenate the result
    k = 0
    for i in range(bucket):
        num = len(arr[i])
        socket_.sleep(speed)
        socket_.emit('buck',{'data':{'algorithm':'BucketSort', 'array':array}}, namespace='/sort')
        for j in range(num):
            # Visualizing the elements being stored to its original array after sorting
            socket_.sleep(speed)
            socket_.emit('buck',{'data':{'algorithm':'BucketSort', 'array':array}}, namespace='/sort')
            array[k] = arr[i][j]             # returning sorted elements from buckets to array
            k += 1

    print("Sorted Array: ", array)
    bucketThread = None

###########################
#########ROUTES############
###########################

@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

###########################
#########SOCKETS###########
###########################

@socket_.on('insertion', namespace='/sort')
def insertion(data):
    message=data['data']
    global insThread
    with ins_thread_lock:
        if insThread is None:
            arr=arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])#[i for i in range(message['max'], message['min']-1, -1)]

            insThread = socket_.start_background_task(insertion_sort, arr, message['speed'])
    emit('logging', {'data': 'Starting insertion sort'})

@socket_.on('selection', namespace='/sort')
def selection(data):
    message=data['data']
    global selThread
    with sel_thread_lock:
        if selThread is None:
            arr=arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])#[i for i in range(message['max'], message['min']-1, -1)]

            selThread = socket_.start_background_task(selection_sort, arr, message['speed'])
    emit('logging', {'data': 'Starting selection sort'})

@socket_.on('quick', namespace='/sort')
def quick(data):
    message=data['data']
    global qckThread
    with qck_thread_lock:
        if qckThread is None:
            arr=arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])#[i for i in range(message['max'], message['min']-1, -1)]

            qckThread = socket_.start_background_task(quick_sort, arr, message['speed'])
    emit('logging', {'data': 'Starting quick sort'})

@socket_.on('heap', namespace='/sort')
def heap(data):
    message=data['data']
    global hepThread
    with hep_thread_lock:
        if hepThread is None:
            arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])#[i for i in range(message['max'], message['min']-1, -1)]
            hepThread = socket_.start_background_task(heap_sort, arr, message['speed'])
    emit('logging', {'data': 'Starting heap sort'})

@socket_.on('radix', namespace='/sort')
def radix(data):
    message=data['data']
    global radThread
    with rad_thread_lock:
        if radThread is None:
            arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])#[i for i in range(message['max'], message['min']-1, -1)]
            radThread = socket_.start_background_task(radix_sort, arr, message['speed'])
    emit('logging', {'data': 'Starting heap sort'})

@socket_.on('BubbleSort', namespace='/sort')
def BubbleSort(data):
    message=data['data']
    global bubbleThread
    with bubble_thread_lock:
        if bubbleThread is None:
            arr=arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])
            bubbleThread =socket_.start_background_task(bubble_sort, arr, message['speed'])
    emit('logging', {'data':'Starting BuubleSort'})

@socket_.on('mergesort', namespace='/sort')
def mergesort(data):
    message= data['data']
    global mergeThread
    with merge_thread_lock:
        if mergeThread is None:
            arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])
            mergeThread = socket_.start_background_task(merge_sort, arr, 0, message['max'], message['speed'])
    emit('logging', {'data': 'Start mergesort'})

@socket_.on('BucketSort', namespace='/sort')
def BucketSort(data):
    message=data['data']
    global bucketThread
    with bucket_thread_lock:
        if bucketThread is None:
            arr=random.sample(range(message['min'], message['max']), message['max']-message['min'])
            bucketThread = socket_.start_background_task(bucket_sort, arr, message['speed'])
    emit('logging', {'data': 'Start BucketSort'})

if __name__ == '__main__':
    socket_.run(app, debug=True)