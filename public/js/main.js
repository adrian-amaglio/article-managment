function dif_due_date_today(time_stamp, today){
	var test = Math.floor(time_stamp/3600/24);
	return (test - today)
}
function parse_date(time_stamp){
	var truc = new Date(time_stamp*1000)
	return (truc.getDate()+"/"+truc.getMonth()+"/"+truc.getFullYear());
}
function nom_categorie(i,date,display){
	console.log(i)
	if(display[i]){
		return(display[i].additional_string)
	}
	return(parse_date((date+i)*24*3600))
}

$(function(){
	var v = new Vue({
		el:"main",
		data:{
			ip: "articles.dahus-host.fr",
			api: "/api/v1.0",
			res : { "step" : {}},
			list : []
		},
		created: function() {
			var url = location.href;
			console.log(url.split("/")[url.split("/").length - 1]);
			if(url.split("/")[url.split("/").length - 2] == "article"){
				this.getArticle(url.split("/")[url.split("/").length - 1]);
			}else {
                this.getArticles();
            }
		},
		methods:{
			date_test : function(truc){
				var date = new Date(truc*1000);
				var hours = date.getHours();
				var minutes = ("0" + date.getMinutes()).substr(-2);
				return(hours+":"+minutes)
			},
			class_due_date : function(time_stamp){
				var deadline_colors = this.res.deadline_colors.sort((a,b)=>{return (b.seconds - a.seconds)});
				var date = Math.floor(Date.now() / 1000);
				for (var i = deadline_colors.length - 1; i >= 0; i--) {
					var data = deadline_colors[i];
					//à tester
					if(dif_due_date_today(time_stamp,Math.floor(date/24/3600)) == 0 && (time_stamp-date) < data.seconds){
						return { color : data.color}
					}
				}
				return "ok"
			},
			nom_categorie : function(i){
				if(this.res.display[i]){
					return(this.res.display[i].additional_string)
				}
				var date =  new Date((Math.floor(Date.now()/1000/3600/24)+parseInt(i))*24*3600*1000)
				return (("0"+date.getDate()).substr(-2)+"/"+("0"+(date.getMonth()+1)).substr(-2)+"/"+date.getFullYear());
			},
			max_length : function(article){
				if (article.format == "article") {
					if(article.max_length > 0){
						return 'Entre <em>'+article.min_length+'</em> et <em>'+article.max_length+'</em> caractères'
					}
					return '<em>∞</em> caractères'
				}
				return 'Entre <em>'+article.min_length+'</em> et <em>'+article.max_length+'</em> secondes'
			},
			repliage : function(){
				return "none"
			},
			getEmissions: function(){
				this.changeStep(10);
			},
			getArticles: function(){
				this.changeStep(0);
			},
			getArticle(id){
                $.get(this.api+'/article/'+id, (res,err) => {
                	this.res = res;
				})
			},
			changeStep: function(step){
                $.get(this.api+'/articles/'+step, (res,err) => {
                    this.res = res;
                    var data = {};
                    var date = Math.floor(Date.now()/1000/3600/24);
                    for (var i = res.articles.length - 1; i >= 0; i--) {
                        const dif_date = dif_due_date_today(res.articles[i].due_date, date);
                        if(data[dif_date]){
                            data[dif_date].push(res.articles[i])
                        }else{
                            data[dif_date] = [res.articles[i]]
                        }
                    }
                    this.list = [];
                    for (i in data) {
                        if (this.res.display[i]) {
                            this.list.push({'key' : i, 'data': data[i], 'display':this.res.display[i].display})
                        }
                        else{
                            this.list.push({'key' : i, 'data': data[i], 'display':false});
                        }
                    }
                    this.list = this.list.sort((a,b)=>{return (a.key - b.key)});
                })
			}
		}
	});
})
