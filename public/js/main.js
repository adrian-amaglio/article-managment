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
	v = new Vue({
		el:"main",
		data:{
			api: "/api/1.0",
			res : { "step" : {}},
			today : [],
			tomorow : [],
			data : {}
		},
		created: function() {
			var url = location.href;
			console.log(url.split("/")[4]);
			$.get('articles.mock.json', (res,err) => {
				this.res = res;
				var date = Math.floor(Date.now()/1000/3600/24);
				for (var i = res.articles.length - 1; i >= 0; i--) {
					j = dif_due_date_today(res.articles[i].due_date, date);
					a = nom_categorie(j,date,res.display)
					if(this.data[j]){
						this.data[j].push(res.articles[i])
					}else{
						this.data[j] = [res.articles[i]]
					}
				}
				console.log(this.data);
				//ca marche pas, faut sort
				this.data = this.data.sort();
			})

		},
		methods:{
			date_test : function(truc){
				var date = new Date(truc*1000);
				var hours = date.getHours();
				var minutes = ("0" + date.getMinutes()).substr(-2);
				return(hours+":"+minutes)
			},
			class_due_date : function(time_stamp){
				deadline_colors = this.res.deadline_colors.sort();
				var date = Math.floor(Date.now() / 1000);
				for (var i = deadline_colors.length - 1; i >= 0; i--) {
					data = deadline_colors[i];
					//à tester
					if(dif_due_date_today(time_stamp,Math.floor(date/24/3600)) == 0 && (time_stamp-date) < data.seconds){
						return { color : data.color}
					}
				}
				return "ok"
			}
			/*
				function nom_categorie(i,date){
					var diplay = res.display
					console.log(i)
					if(display[i]){
						return(display[i].additional_string)
					}
					return(parse_date((date+i)*24*3600))
				}
				function parse_date(time_stamp){
					var truc = new Date(time_stamp*1000)
					return (truc.getDate()+"/"+truc.getMonth()+"/"+truc.getFullYear());
				}
				
			*/
		}
	});
})