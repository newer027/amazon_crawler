function VOL_MEASURES() {
	this.mCubic_meter = 1000
	this.mHectoliter = 100
	this.mDekaliter = 10
	this.mLiter = 1
	this.mDeciliter = 0.1
	this.mCentiliter = 0.01
	this.mMilliliter = 0.001
	this.mCubic_millimeter = 0.000001
	this.mcTable_spoon= 0.015
	this.mcTea_spoon= 0.005
	this.uscCubic_inch = 0.016387064
	this.uscAcre_foot = 43560 * 1728 * this.uscCubic_inch
	this.uscCubic_yard = 27 * 1728 * this.uscCubic_inch
	this.uscCubic_foot = 1728 * this.uscCubic_inch
	this.uslGallon = 231 * this.uscCubic_inch
	this.uslBarrel = 42 * this.uslGallon
	this.uslQuart =  this.uslGallon / 4
	this.uslPint =  this.uslGallon / 8
	this.uslGill =  this.uslGallon / 32
	this.uslFluid_ounce = this.uslGallon / 128
	this.uslFluid_dram =  this.uslGallon / 1024
	this.uslMinim = this.uslFluid_ounce / 61440
	this.usdBarrel = 7056 * this.uscCubic_inch
	this.usdBushel = 2150.42 * this.uscCubic_inch
	this.usdPeck = this.usdBushel / 4
	this.usdQuart = this.usdBushel / 32
	this.usdPint = this.usdBushel / 64
	this.uscCup = 8 * this.uslFluid_ounce
	this.uscTable_spoon = this.uslFluid_ounce / 2
	this.uscTea_spoon = this.uslFluid_ounce / 6
	this.briGallon = 4.54609
	this.briBarrel = 36 * this.briGallon
	this.briBushel = 8  * this.briGallon
	this.briPint = this.briGallon / 8
	this.briFluid_ounce = this.briGallon / 160
}
var vol_data = new VOL_MEASURES();
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
			if (c>=5) {
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
		}
		else
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
	resetValues(form,vol_data);
}
