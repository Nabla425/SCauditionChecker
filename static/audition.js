const app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data: {
        settings: {},
        situation: {},
        history: [],
        isFinish: false,
        result: {},
        all_deck: [],
        selectedDeckIdx: 0,
        editing: false,
        isEditAudition: false,
        audition_names: [
            "夕方ワイドアイドル一番", "エレぇベスト", "SPOT LIGHTのせいにして…", "踊っていいとも？創刊号",
            "THE LEGEND", "七彩メモリーズ", "歌姫楽宴"
        ],
        season: [0, 0],
        trend:['','','']
    },
    mounted() {
        const settings = localStorage.getItem('settings');
        const situation = localStorage.getItem('situation');
        
        if (settings && situation) {
            this.settings = JSON.parse(settings);
            this.situation = JSON.parse(situation);
            this.season[0] = Math.floor(this.settings.week / 8);
            this.season[1] = this.settings.week % 8;
            fetch('/api/changePassive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.settings.aquired_passive)
            })
            .then(response => response.json())
            .then(data => {
                this.situation.passive_list = data;
                this.trend[this.settings.trend.Vo-1] = 'Vo';
                this.trend[this.settings.trend.Da-1] = 'Da';
                this.trend[this.settings.trend.Vi-1] = 'Vi';
            });
        } else {
            fetch('/api/init')
            .then(response => response.json())
            .then(data => {
                this.settings = data.settings;
                this.situation = data.situation;
                console.log(JSON.stringify(this.situation, null, 2));
                console.log(JSON.stringify(this.settings, null, 2));

                this.season[0] = Math.floor(this.settings.week / 8);
                this.season[1] = this.settings.week % 8;

                this.trend[this.settings.trend.Vo-1] = 'Vo';
                this.trend[this.settings.trend.Da-1] = 'Da';
                this.trend[this.settings.trend.Vi-1] = 'Vi';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        
        fetch('/api/all_deck')
        .then(response => response.json())
        .then(data => {
            this.all_deck = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Initialize Sortable
        this.initSortable();
    },
    computed: {
        selectedDeck() {
            return this.all_deck[this.selectedDeckIdx] || {};
        }
    },
    watch: {
        season: {
            handler(newVal) {
                this.settings.week = (newVal[0] - 1) * 8 + newVal[1];
            },
            deep: true
        },
    },
    methods: {
        handleSubmit() {
            this.history.push(JSON.parse(JSON.stringify(this.situation)));

            const data = {
                form: Object.fromEntries(new FormData(document.querySelector('form'))),
                situation: this.situation,
                settings: this.settings
            };

            fetch('/api/turn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Received data:', JSON.stringify(data, null, 2));
                this.settings = data.settings;
                this.situation = data.situation;
                this.result = data.result;
                if(data.isEnd){
                    document.getElementById('endScreen').style.display = 'flex';
                    console.log(this.result)
                    this.drawChart('Vo');
                    this.drawChart('Da');
                    this.drawChart('Vi');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        back() {
            document.getElementById('endScreen').style.display = 'none';
            if (this.history.length > 0) {
                this.situation = this.history.pop();
            }
        },
        reset() {
            document.getElementById('endScreen').style.display = 'none';
            fetch('/api/init')
            .then(response => response.json())
            .then(data => {
                this.situation = data.situation;
                this.history = [];
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        editPage() {
            localStorage.setItem('settings', JSON.stringify(this.settings));
            localStorage.setItem('situation', JSON.stringify(this.situation));
            window.location.href = '/edit';
        },
        saveSelection() {
            this.editing = false;
            let deck_id = this.all_deck[this.selectedDeckIdx].deck_id;
            fetch(`/api/setDeck/${deck_id}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.settings = { ...this.settings, ...data.settings };
                    this.situation.passive_list = data.passive_list;
                });
        },
        deleteDeck(deck) {
            if (confirm(deck.name + ' を削除しますか？')) {
                console.log(deck);
                fetch(`/api/deleteDeck/${deck.id}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        this.all_deck = this.all_deck.filter(d => d.id !== deck.id);
                        if (this.selectedDeckIdx !== null && this.all_deck.length > 0) {
                            this.selectedDeckIdx = this.all_deck[0].id;
                        } else {
                            this.selectedDeckIdx = null;
                        }
                    });
            }
        },
        toggleEditAudition() {
            if (this.isEditAudition) {
                // 1位、2位、3位の属性にかぶりがないか確認
                const trend = [this.trend[0], this.trend[1], this.trend[2]];
                const uniqueTrends = new Set(trend);
        
                if (uniqueTrends.size === 3) {
                    // かぶりがない場合、settings.trendに保存して設定をリロード、editAuditionをfalseに戻す
                    this.settings.trend = {
                        [this.trend[0]]: 1,
                        [this.trend[1]]: 2,
                        [this.trend[2]]: 3
                    };
                    this.reloadAudition() 
                    this.isEditAudition = false;
                } else {
                    // かぶりがある場合、editAuditionをtrueのままにしてアラートを表示
                    this.isEditAudition = true;
                    alert('流行に重複した順位があります。設定しなおしてください');
                }
            } else {
                this.isEditAudition = true;
            }
        },
        reloadAudition() {
            fetch('/api/reload_audition', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"settings": this.settings, "situation": this.situation})
            })
            .then(response => response.json())
            .then(data => {
                this.settings = data.settings;
                this.situation = data.situation;
            });
        },
        drawChart(col) {
            const appealScores = this.situation.judge_dict[col].score.appeal;
            const labels = Object.keys(appealScores);
            const data = Object.values(appealScores);

            var ctx = document.getElementById(col+'PieChart').getContext('2d');
            var myPieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        },
        
    }
});
