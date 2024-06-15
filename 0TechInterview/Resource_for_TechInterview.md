# Tech Interview Resources

 ## Global resources

- [📔Tech Interview Handbook](https://www.techinterviewhandbook.org/)
> **Best Roadmap**
> Direct roadmap to help you prepare for a technical interview and land a **FAANG** job.

 - [🎓Coding interview University](https://github.com/jwasham/coding-interview-university)
> **Best collection of resources** 
> Collection of all possible resources with really good articles and explenations.
 
- [🚀NeetCode.io](https://neetcode.io/) 
> **Best tutorials and Roadmap for LeetCode level up**

## 🇺🇦 Ukrainian Resources

- [📚 Dou.ua: Как попасть в Google: инструкция по подготовке by *Sergi Semi*](https://dou.ua/lenta/articles/google-interview/)

- [📚 Dou.ua: Как я искал работу в США во время пандемии, подался на 200 вакансий и получил оффер на $380K by *Adam Leos*](https://dou.ua/lenta/interviews/get-job-in-usa-during-pandemic/)



## Best Youtube Channels

![Pirate King](./img/YT_PirateKing.webp)
- [Pirate King](https://www.youtube.com/watch?v=17cQGPLbmfQ)
> Good guides and overall strategies for coding interviews.

![Joma Tech YT](./img/YT_JomaTech.webp)
- [Joma Tech](https://www.youtube.com/watch?v=5bId3N7QZec)
> Fun and informative a lot of good interviews with software engineers.

![ThePrimeagen](./img/YT_ThePrmeagen.webp)
- [ThePrimeagen](https://www.youtube.com/watch?v=hW5s_UUO1RI)
> ♂ 💪 **REAL** ♂ 💪 **MALE** way of coding & 🥲 fun to watch if you love pain and VIM.

## Example code

NO it's comletely diffent infomration 

```python
def BFS(graph, start):
    visited = set()
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited
```
```rust 
fn bfs(graph: &HashMap<i32, Vec<i32>>, start: i32) -> HashSet<i32> {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back(start);
    while let Some(vertex) = queue.pop_front() {
        if !visited.contains(&vertex) {
            visited.insert(vertex);
            for &neighbour in &graph[&vertex] {
                if !visited.contains(&neighbour) {
                    queue.push_back(neighbour);
                }
            }
        }
    }
    visited
}
```
