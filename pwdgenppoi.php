pwdgenppoi for php<BR>
<form name="pwdgenppoi" action="./" method="POST">
mkey:<input type="password" name="masterkey"><BR>
skey:<input type="text" name="subkey"><BR>
klen:<input type="text" name="length" value="16" maxlength="2" size="2"> type:<select name="key_type">
 <option value="1">09azAZSym
 <option value="2">09azAZ
 <option value="3">09az
 <option value="4">09
</select> 
<input type="submit" value=" Go "></form><BR>
<?
function nencode($num, $chars) {
	$str = "";
	switch ($chars) {
		case "1":
			$chars = strval("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ#$-=?@[]_");
			break;
		case "2":
			$chars = strval("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ");
			break;
		case "3":
			$chars = strval("0123456789abcdefghijklmnopqrstuvwxyz");
			break;
		case "4":
			$chars = strval("0123456789");
			break;
	}
	while ($num != 0) {
		$point = bcmod($num,strlen($chars));
		$str = substr($chars, $point, 1). $str;
		$num = bcdiv(bcsub($num,bcmod($num,strlen($chars))),strlen($chars));
	}
	return $str;
}

function superh2d($hexnum) {
	$dec = "0";
	$point = 0;
	while (strlen($hexnum) != $point) {
		$dec = bcadd(base_convert($hexnum{$point},16,10),bcmul($dec,"16"));
		$point = $point + 1;
	}
	return $dec;
}

$pwd = nencode(bcmul(superh2d(sha1($_POST["masterkey"])),superh2d(md5($_POST["subkey"]))),$_POST["key_type"]);
$pwd = substr($pwd,5,$_POST["length"]);
if (preg_match("/[0-9]/", $pwd)) {
}
else {
        $pwd = substr($pwd,0,$_POST["length"] - 1). substr(superh2d(md5($pwd)),4,1);
}

echo 'pwd:<input type="text" name="pwd" value="'. $pwd. '">';
?>