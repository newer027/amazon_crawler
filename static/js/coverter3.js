function AREA_MEASURES()
{
	this.mSquare_kilometer = (1000 * 1000)
	this.mHectare = (100 * 100)
	this.mSquare_meter = 1
	this.mAre = ((10000/15) * this.mSquare_meter)
	this.mSquare_decimeter = (0.1 * 0.1)
	this.mSquare_centimeter = (0.01 * 0.01)
	this.mSquare_millimeter = (0.001 * 0.001)
	this.engSquare_foot = (0.3048 * 0.3048)
	this.engSquare_yard = (3 * 3 * this.engSquare_foot)
	this.usSquare_rod = (16.5 *16.5 * this.engSquare_foot)
	this.engAcre = 160 * this.usSquare_rod
	this.engSquare_mile = (5280 *5280 * this.engSquare_foot)
	this.engSquare_inch = (this.engSquare_foot / (12 * 12))
}
var area_data = new AREA_MEASURES();
function checkNum(str) {
	for (var i=0; i<str.length; i++) {
		var ch = str.substring(i, i + 1)
		if (ch!="." && ch!="+" && ch!="-" && ch!="e" && ch!="E" && (ch < "0" || ch > "9")) {
			alert("请输入有效的数字");
			return false;
		}
	}
	return true
}
function normalize(what,digits) {
	var str=""+what;
	var pp=Math.max(str.lastIndexOf("+"),str.lastIndexOf("-"));
	var idot=str.indexOf(".");
	if (idot>=1) {
		var ee=(pp>0)?str.substring(pp-1,str.length):"";
		digits+=idot;
		if (digits>=str.length)
			return str;
				if (pp>0 && digits>=pp)
			digits-=pp;
		var c=eval(str.charAt(digits));
		var ipos=digits-1;
		if (c>=5)  {
			while (str.charAt(ipos)=="9")
				ipos--;
			if (str.charAt(ipos)==".") {
				var nc=eval(str.substring(0,idot))+1;
				if (nc==10 && ee.length>0) {
					nc=1;
					ee="e"+(eval(ee.substring(1,ee.length))+1);
				}
				return ""+nc+ee;
			}
			return str.substring(0,ipos)+(eval(str.charAt(ipos))+1)+ee;
		} else
			var ret=str.substring(0,digits)+ee;
		for (var i=0; i<ret.length; i++)
				if (ret.charAt(i)>"0" && ret.charAt(i)<="9")
					return ret;
		return str;
	}
	return str;
}
function compute(obj,val,data) {
	if (obj[val].value) {
		var uval=0;
		uval = obj[val].value*data[val];
		if( (uval >= 0) && (obj[val].value.indexOf("-") != -1) ) {
			uval = -uval;    // *** Hack for Opera 4.0  2000-10-14
		}
		for (var i in data)
			obj[i].value=normalize(uval/data[i],8);
	}
}
function resetValues(form,data) {
		for (var i in data)
			form[i].value="";
}

function resetAll(form) {
	resetValues(form,area_data);
}
