        class Graph {
            constructor() {
                this.graph = {};
                this.vertices = new Set();
                this.s = null;
                this.t = null;
            }

            parseGraphFromFile(content) {
                const lines = content.split('\n').map(line => line.trim()).filter(line => line);

                if (lines.length < 2) {
                    throw new Error('Файл должен содержать как минимум начальную и конечную вершины');
                }

                this.s = lines[0];
                this.t = lines[1];
                this.graph = {};
                this.vertices = new Set([this.s, this.t]);

                for (let i = 2; i < lines.length; i++) {
                    const parts = lines[i].split(/\s+/);
                    if (parts.length < 3) continue;

                    const u = parts[0];
                    const v = parts[1];

                    this.vertices.add(u);
                    this.vertices.add(v);
                }

                for (let i = 2; i < lines.length; i++) {
                    const parts = lines[i].split(/\s+/);
                    if (parts.length < 3) continue;

                    const u = parts[0];
                    const v = parts[1];
                    const weight = parseInt(parts[2]);

                    if (isNaN(weight)) {
                        throw new Error(`Неверный вес в строке ${i + 1}: ${parts[2]}`);
                    }

                    if (!this.graph[u]) {
                        this.graph[u] = [];
                    }
                    this.graph[u].push([v, weight]);
                }

                this.vertices.forEach(vertex => {
                    if (!this.graph[vertex]) {
                        this.graph[vertex] = [];
                    }
                });

                return this;
            }

            topologicalSort() {
                const color = {};
                const stack = [];
                const order = [];
                const processSteps = [];

                this.vertices.forEach(vertex => {
                    color[vertex] = 'white';
                });

                stack.push(this.s);

                while (stack.length > 0) {
                    const v = stack[stack.length - 1];
                    processSteps.push(`Вершина на вершине стека: ${v}, цвет: ${color[v]}`);

                    if (color[v] === 'white') {
                        color[v] = 'gray';
                        processSteps.push(`→ Покрасили ${v} в серый`);

                        let addedAny = false;
                        if (this.graph[v]) {
                            for (const [neighbor] of this.graph[v]) {
                                if (color[neighbor] === 'white') {
                                    stack.push(neighbor);
                                    processSteps.push(`→ Добавили в стек белую вершину ${neighbor}`);
                                    addedAny = true;
                                }
                            }
                        }

                        if (!addedAny) {
                            processSteps.push(`→ У вершины ${v} нет белых соседей`);
                        }
                    }
                    else if (color[v] === 'gray') {
                        stack.pop();
                        color[v] = 'black';
                        order.push(v);
                        processSteps.push(`→ Извлекли ${v} из стека, покрасили в черный, добавили в топологическую сортировку`);
                    }
                    else {
                        stack.pop();
                        processSteps.push(`→ Вершина ${v} уже черная, извлекаем из стека`);
                    }
                }

                order.reverse();
                processSteps.push(`Топологический порядок: ${order.join(' → ')}`);

                return { order, processSteps };
            }

            longestPath() {
                const { order, processSteps } = this.topologicalSort();

                if (!order.includes(this.s) || !order.includes(this.t)) {
                    return { path: null, length: -Infinity, processSteps };
                }

                const idx_s = order.indexOf(this.s);
                const idx_t = order.indexOf(this.t);

                if (idx_s > idx_t) {
                    return { path: null, length: -Infinity, processSteps };
                }

                const OPT = {};
                const X = {};

                this.vertices.forEach(vertex => {
                    OPT[vertex] = -Infinity;
                    X[vertex] = null;
                });

                OPT[this.s] = 0;
                processSteps.push(`Обрабатываем вершину ${this.s}: OPT[${this.s}] = ${OPT[this.s]}`);

                for (let i = idx_s + 1; i <= idx_t; i++) {
                    const currentVertex = order[i];

                    processSteps.push(`Обрабатываем вершину ${currentVertex}:`);

                    let maxValue = -Infinity;
                    let bestPred = null;
                    let options = [];

                    for (const u of order.slice(0, i)) {
                        if (this.graph[u]) {
                            for (const [v, weight] of this.graph[u]) {
                                if (v === currentVertex && OPT[u] !== -Infinity) {
                                    const candidateValue = OPT[u] + weight;
                                    options.push(`${u} → ${currentVertex}: ${OPT[u]} + ${weight} = ${candidateValue}`);

                                    if (candidateValue > maxValue) {
                                        maxValue = candidateValue;
                                        bestPred = u;
                                    }
                                }
                            }
                        }
                    }

                    options.forEach(option => {
                        processSteps.push(`  ${option}`);
                    });

                    if (maxValue > -Infinity) {
                        OPT[currentVertex] = maxValue;
                        X[currentVertex] = bestPred;
                        processSteps.push(`Установили OPT[${currentVertex}] = ${maxValue}, X[${currentVertex}] = ${bestPred}`);
                    } else {
                        processSteps.push(`Нет достижимых предшественников для вершины ${currentVertex}`);
                    }
                }

                if (OPT[this.t] === -Infinity) {
                    processSteps.push(`Вершина ${this.t} недостижима из ${this.s}`);
                    return { path: null, length: -Infinity, processSteps };
                }

                const path = [];
                let current = this.t;
                while (current !== null) {
                    path.push(current);
                    current = X[current];
                }
                path.reverse();

                processSteps.push(`Найден путь: ${path.join(' → ')}, длина: ${OPT[this.t]}`);

                return { path, length: OPT[this.t], processSteps };
            }

            getGraphInfo() {
                let edgeCount = 0;
                for (const u in this.graph) {
                    edgeCount += this.graph[u].length;
                }

                return {
                    vertices: this.vertices.size,
                    edges: edgeCount,
                    start: this.s,
                    end: this.t
                };
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            const fileInput = document.getElementById('fileInput');
            const uploadArea = document.getElementById('uploadArea');
            const calculateBtn = document.getElementById('calculateBtn');
            const results = document.getElementById('results');
            const graphInfo = document.getElementById('graphInfo');
            const processInfo = document.getElementById('processInfo');
            const pathResult = document.getElementById('pathResult');
            const lengthResult = document.getElementById('lengthResult');

            const graphProcessor = new Graph();

            uploadArea.addEventListener('click', () => fileInput.click());

            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    handleFile(file);
                }
            });

            calculateBtn.addEventListener('click', calculateLongestPath);

            function handleFile(file) {
                if (!file.name.endsWith('.txt')) {
                    alert('Пожалуйста, выберите текстовый файл (.txt)');
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        graphProcessor.parseGraphFromFile(e.target.result);
                        displayGraphInfo();
                        calculateBtn.disabled = false;
                        results.style.display = 'block';

                    } catch (error) {
                        showError('Ошибка при чтении файла: ' + error.message);
                    }
                };
                reader.readAsText(file);
            }

            function displayGraphInfo() {
                const info = graphProcessor.getGraphInfo();
                graphInfo.innerHTML = `
                    <div class="result-item">
                        <strong>Начальная вершина:</strong> ${info.start}
                    </div>
                    <div class="result-item">
                        <strong>Конечная вершина:</strong> ${info.end}
                    </div>
                    <div class="result-item">
                        <strong>Количество вершин:</strong> ${info.vertices}
                    </div>
                    <div class="result-item">
                        <strong>Количество рёбер:</strong> ${info.edges}
                    </div>
                `;
            }

            function calculateLongestPath() {
                try {
                    const { path, length, processSteps } = graphProcessor.longestPath();
                    displayProcessInfo(processSteps);
                    displayResults(path, length);

                } catch (error) {
                    showError('Ошибка при вычислении пути: ' + error.message);
                }
            }

            function displayProcessInfo(processSteps) {
                let stepsHTML = '<div class="process-steps"><strong>Процесс выполнения:</strong><br>';
                processSteps.forEach(step => {
                    stepsHTML += `<div class="step">${step}</div>`;
                });
                stepsHTML += '</div>';
                processInfo.innerHTML = stepsHTML;
            }

            function displayResults(path, length) {
                if (path === null || path.length === 0) {
                    pathResult.innerHTML = '<div class="error">Вершина недостижима из начальной вершины</div>';
                    lengthResult.innerHTML = '';
                } else {
                    const pathHTML = path.map((vertex, index) => {
                        const step = `<span style="display: inline-block; padding: 8px 15px; margin: 2px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 15px; font-weight: bold;">${vertex}</span>`;
                        return index < path.length - 1 ? step + '<span style="margin: 0 10px; color: #667eea; font-weight: bold;">→</span>' : step;
                    }).join('');

                    pathResult.innerHTML = '<strong>Найденный путь:</strong><div class="path-display" style="text-align: center;">' + pathHTML + '</div>';
                    lengthResult.innerHTML = `<div class="length-display">Длина пути: ${length}</div>`;
                }

                results.scrollIntoView({ behavior: 'smooth' });
            }

            function showError(message) {
                graphInfo.innerHTML = '';
                processInfo.innerHTML = '';
                pathResult.innerHTML = `<div class="error">${message}</div>`;
                lengthResult.innerHTML = '';
                results.style.display = 'block';
                results.scrollIntoView({ behavior: 'smooth' });
            }
        });
