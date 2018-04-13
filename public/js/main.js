$(function(){
	v = new Vue({
		el:"main",
		data:{
			api: "/api/1.0",
			res : {}
		},
		created:function(){
			$.get('articles.mock.json', (res,err) => {
				this.res = res;
			})

		},
		methods:{
		}
	});
})