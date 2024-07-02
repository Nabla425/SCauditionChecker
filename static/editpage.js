const app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data: {
        settings: {},
        situation: {},
        session:null,
        all_idol: [
            "櫻木真乃", "風野灯織", "八宮めぐる", "月岡恋鐘", "田中摩美々", "白瀬咲耶", "三峰結華", "幽谷霧子",
            "小宮果穂", "園田智代子", "西城樹里", "杜野凛世", "有栖川夏葉", "大崎甘奈", "大崎甜花", "桑山千雪",
            "芹沢あさひ", "黛冬優子", "和泉愛依", "浅倉透", "樋口円香", "市川雛菜", "福丸小糸",
            "七草にちか", "緋田美琴", "斑鳩ルカ", "鈴木羽那", "郁田はるき"
        ],
        buff_form: { color: "", buff: 0, turn: 0, name: "", val: null },
        Sid:0,
        Pid:0,
        all_passive:[],
        all_pweapon:[],
        passive_template:{"card_name":"","icon":"","passive_type":"","times":0,"p":0,"buff":[],"request":"","args":""},
        request_list: ['無条件','3色バフ条件','(属性)UPが付与されている場合','(N)ターン以前','(N)ターン以後','履歴に(アイドル)がある場合','それ以外'],
        passive_rate:["",0],
        args_explain:{
            '無条件':"",
            '3色バフ条件':"",
            '(属性)UPが付与されている場合':"Vo,Da,Vi,At(注目度),Av(回避率)パッシブ発動率(Pa)",
            '(N)ターン以前':"N",
            '(N)ターン以後':"N",
            '履歴に(アイドル)がある場合':"櫻木真乃,風野灯織",
            'それ以外':"各tに鳴く確率　0.3,0.2,0.1,0.8"
        },
        message:null,
        isSearchSupport:true,
        isSearchPweapon:true,
        isEditPassive:false,
        all_support:[],
        Serching_support: {
            idol: '',
            name: '',
            totu: ''
        },
    },
    mounted() {
        const savedSettings = localStorage.getItem('settings');
        const savedSituation = localStorage.getItem('situation');

        if (savedSettings) {
            this.settings = JSON.parse(savedSettings);
            console.log(JSON.stringify(this.settings, null, 2));
        }
        if (savedSituation) {
            this.situation = JSON.parse(savedSituation);
            console.log(JSON.stringify(this.situation, null, 2));
        }
        this.fetch_pweapon_passive();
        this.fetch_session();
        fetch('api/all_support')
        .then(response => response.json())
        .then(data => {
            this.all_support = data
        })

    },
    computed: {
        filteredByIdol() {
            return this.all_support.filter(support => support.idol_name === this.Serching_support.idol);
        },
        filteredByCard() {
            return this.filteredByIdol.filter(support => support.card_name === this.Serching_support.name);
        }
    },
    methods: {
        showSupportInfo(support) {
            this.buff_form.name = (support.card_name + "("+ support.card_type +")")
            this.editing_support = { ...support };
        },
        add_buff(target) {
            if (this.buff_form.color && this.buff_form.buff && this.buff_form.turn) {
                target.push({ ...this.buff_form });
                this.buff_form = { color: "", buff: 0, turn: 0, name: "", val: null };
            }
        },
        remove_buff(buff, target) {
            const index = target.indexOf(buff);
            if (index !== -1) {
                target.splice(index, 1);
            }
        },
        add_passive_buff() {
            this.passive_template.buff.push([ ...this.passive_rate ]);
            this.passive_rate = ["",0];
            
        },
        remove_passive_buff(buff) {
            const index = this.passive_template.buff.indexOf(buff);
            if (index !== -1) {
                this.passive_template.buff.splice(index, 1);
            }
        },
        prepare_link_form(target){
            console.log(target.link_type)
            if(target.link_type=="ATK"){
                target.link_contents = {"Vo":0,"Da":0,"Vi":0};
            }
            else if(target.link_type=="buff"){
                target.link_contents = [];
                console.log(target.link_contents);
            }
            else if(target.link_type=="no_link"){
                target.link_contents = "no_link";
            }
        },
        fetch_pweapon_passive(){
            let deck_list = [[this.settings.produce_idol,this.settings.produce_card]]
            for (let support of this.settings.support_list) { 
                deck_list.push([support.idol_nmae,support.card_name]); 
            }
            fetch('/api/fetchPweaponPaassive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(deck_list) 
            })
            .then(response => response.json())  
            .then(data => {
                this.all_passive = data.all_passive;
                this.all_pweapon = data.all_pweapon;
            })
        },

        fetch_session(){
            fetch('api/session')
            .then(response => response.json())
            .then(data => {
                this.session = data
            })
        },
        submit_support(){
            fetch('/api/pushSupport', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(this.settings.support_list[this.Sid]) 
            })
            .then(response => response.json())  
            .then(data => {
                this.message = data.message;
                alert(data.message)
            })
        },
        submit_pweapon(){
            fetch('/api/pushPweapon', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(this.settings.pweapon_list[this.Pid]) 
            })
            .then(response => response.json())  
            .then(data => {
                this.message = data.message;
                alert(data.message)
            })
        },
        submit_passive(){
            fetch('/api/pushPassive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(this.passive_template) 
            })
            .then(response => response.json())  
            .then(data => {
                this.message = data.message;
                alert(data.message)
            })
            this.passive_template.args = '';
        },
        submit_deck(){
            fetch('/api/pushDeck', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(this.settings) 
            })
            .then(response => response.json())  
            .then(data => {
                this.message = data.message;
                alert(data.message)
            })
        },
        submit_Pcard(){
            fetch('/api/pushPcard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({idol:this.settings.produce_idol,cardname:this.settings.produce_card}) 
            })
            .then(response => response.json())  
            .then(data => {
                this.message = data.message;
                alert(this.message)
            })
        },
        return_simulation(){
            localStorage.setItem('settings', JSON.stringify(this.settings));
            localStorage.setItem('situation', JSON.stringify(this.situation));
            window.location.href = '/audition'
        },
        updateSupport() {
            const selectedSupport = this.all_support.find(support =>
            support.idol_name === this.Serching_support.idol &&
            support.card_name === this.Serching_support.name &&
            support.totu === this.Serching_support.totu
        );
        if (selectedSupport) {
            this.settings.support_list[this.Sid] = selectedSupport;
            }
        },
        toggle_edit_passive(){
            this.isEditPassive = !this.isEditPassive;
        }
    }
});