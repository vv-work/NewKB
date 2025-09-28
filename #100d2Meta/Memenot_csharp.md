
```csharp

PriorityQueue<int,int> heap = new PriorityQueue<int,int>(
	 counter.Select(kvp => (kvp.Key, -kvp.Value)) // negative for max-heap behavior
);

```
```csharp
int [] arr = {1,2,3,4,5};
arr.Sum(); // 15
arr.Max(); // 5
arr.Min(); // 1


// Convert char to int
char c = '5';
int number = c - '0';  // 5

// StringBuilder
StringBuilder sb = new StringBuilder();
sb.Append('a');

PriorityQueue<int> pq = new PriorityQueue<int>();
pq.Enqueue(5);


```

## Tricks with chars 


```csharp
  
if (s.Length != t.Length)
	return false;

  

int [] letters = new int [26];
for (int i = 0; i<s.Length; i++){

	int l1 = s[i]-'a';
	int l2 = t[i]-'a';
	
	letters[l1]++;
	letters[l2]--;
}


foreach(var l in letters){
	if (l!=0)
		return false;

}

return true;
```


## Getting group anagram 

```csharp
public IList<IList<string>> GroupAnagrams(string[] strs) {

	var dict = new Dictionary<string,IList<string>>();
	for(int i = 0; i <strs.Length; i++){
	
		var s = strs[i];
		var key = new string(s.OrderBy(x=>x).ToArray());
		
		if (!dict.ContainsKey(key))
			dict[key] = new List<string>();
		
		dict[key].Add(s);
	
	}
	
	return dict.Values.ToList();

}
```