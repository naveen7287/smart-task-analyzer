async function analyzeTasks(){
  const input = document.getElementById('taskInput').value;
  const strategy = document.getElementById('strategy').value;
  let tasks = [];
  try {
    tasks = JSON.parse(input);
  } catch (e) {
    alert('Invalid JSON. Please fix it.');
    return;
  }
  try {
    const resp = await fetch('/api/tasks/analyze/?strategy='+strategy, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(tasks)
    });
    const data = await resp.json();
    renderResults(data);
  } catch (e) {
    alert('Request failed: '+e);
  }
}

async function suggestTasks(){
  const input = document.getElementById('taskInput').value;
  const strategy = document.getElementById('strategy').value;
  let tasks = [];
  try {
    tasks = JSON.parse(input);
  } catch (e) {
    alert('Invalid JSON. Please fix it.');
    return;
  }
  try {
    const resp = await fetch('/api/tasks/suggest/?strategy='+strategy, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(tasks)
    });
    const data = await resp.json();
    const r = document.getElementById('results');
    r.innerHTML = '<div class="alert alert-info">'+data.explanation+'</div>';
    data.top.forEach(item=>{
      const card = makeCard(item.task, item.score, item.breakdown);
      r.appendChild(card);
    });
  } catch (e) {
    alert('Request failed: '+e);
  }
}

function renderResults(tasks){
  const r = document.getElementById('results');
  r.innerHTML = '';
  tasks.forEach(t=>{
    const card = makeCard(t, t.score, t.breakdown);
    r.appendChild(card);
  });
}

function makeCard(task, score, breakdown){
  const col = document.createElement('div');
  col.className = 'col-12';
  const card = document.createElement('div');
  card.className = 'card p-3 card-task';
  if(score>70) card.classList.add('priority-high');
  else if(score>40) card.classList.add('priority-med');
  else card.classList.add('priority-low');
  const title = document.createElement('h5');
  title.innerText = task.title || '(no title)';
  const meta = document.createElement('div');
  meta.innerHTML = '<small>Score: '+Math.round(score)+'</small> • <small>Due: '+(task.due_date||'—')+'</small>';
  const body = document.createElement('pre');
  body.innerText = JSON.stringify(breakdown, null, 2);
  card.appendChild(title);
  card.appendChild(meta);
  card.appendChild(body);
  col.appendChild(card);
  return col;
}
