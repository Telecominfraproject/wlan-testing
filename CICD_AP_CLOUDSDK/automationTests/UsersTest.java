package automationTests;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;

import org.junit.AfterClass;
import org.junit.Test;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

import java.util.Map;

public class UsersTest{
	WebDriver driver;
	static APIClient client;
	static long runId;
	
//	static String Url = System.getenv("CLOUD_SDK_URL");
//	static String trUser = System.getenv("TR_USER");
//	static String trPwd = System.getenv("TR_PWD");
//	static String cloudsdkUser = "support@example.com";
//	static String cloudsdkPwd="support";
	@BeforeClass
	public static void startTest() throws Exception
	{
		client = new APIClient("https://telecominfraproject.testrail.com");
		client.setUser("syama.devi@connectus.ai");
		client.setPassword("Connect123$");
		JSONArray c = (JSONArray) client.sendGet("get_runs/5");
		runId = new Long(0);
		
		Calendar cal = Calendar.getInstance();
		//Months are indexed 0-11 so add 1 for current month
		int month = cal.get(Calendar.MONTH) + 1;
		String day = Integer.toString(cal.get(Calendar.DATE));
		if (day.length()<2) {
			day = "0"+day;
		}
		String date = "UI Automation Run - " + day + "/" + month + "/" + cal.get(Calendar.YEAR);
		
		for (int a = 0; a < c.size(); a++) {
			if (((JSONObject) c.get(a)).get("name").equals(date)) {
				runId =  (Long) ((JSONObject) c.get(a)).get("id"); 
			}
		}
	}
	
	public void launchBrowser() {
		System.setProperty("webdriver.chrome.driver", "/home/netex/nightly_sanity/ui-scripts/chromedriver");
//		System.setProperty("webdriver.chrome.driver", "/Users/mohammadrahman/Downloads/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--no-sandbox");
		options.addArguments("--headless");
		options.addArguments("--window-size=1920,1080");
		driver = new ChromeDriver(options);
		driver.get("https://wlan-ui.qa.lab.wlan.tip.build");
	}
	
	void closeBrowser() {
		driver.close();
	}
	
	public void logIn() {
		driver.findElement(By.id("login_email")).sendKeys("support@example.com");
		driver.findElement(By.id("login_password")).sendKeys("support");
		driver.findElement(By.xpath("//*[@id=\"login\"]/button/span")).click();
	}
	
	public void failure(int testId) throws MalformedURLException, IOException, APIException {
		driver.close();
		Map data = new HashMap();
		data.put("status_id", new Integer(5));
		data.put("comment", "Fail");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	
	public void accountsScreen(int testId) throws Exception {
		try {
			driver.findElement(By.linkText("Users")).click();
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	public void addAccountButton(int testId) throws MalformedURLException, IOException, APIException {
		try {
			Actions act =  new Actions(driver);
			act.moveToElement(driver.findElement(By.cssSelector("[title^='addaccount']"))).click().perform();
		}  catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	public void verifyAddAccountPopup(int testId) throws MalformedURLException, IOException, APIException {
		Map data = new HashMap();
		try {
			if (driver.findElement(By.id("rcDialogTitle0")).getText().equals("Add User")) {
				//pass
			} else {
				
				failure(testId);
				fail();
			}
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}	
	}
	
	public void addAccount(String account, String password, String confirmPassword, int testId) throws MalformedURLException, IOException, APIException {
		try {
			addAccountButton(testId);
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(account).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(password).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(confirmPassword).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	public void blankEmailWarning(int testId) throws Exception {
		try {
			if (driver.findElement(By.cssSelector("[role^='alert']")).getText().equals("Please input your e-mail")) {
				//pass
			} else {
				
				failure(testId);
				fail("Incorrect warning displayed");
			}
		} catch (Exception E) {
			failure(testId);
			fail("No warning displayed");
		}
	}
	
	public void invalidPasswordsWarning(int testId) throws Exception {
		try {
			if (driver.findElement(By.cssSelector("[role^='alert']")).getText().equals("The two passwords do not match")) {
				//pass
			} else {
				
				failure(testId);
				fail("Incorrect warning displayed");
			}
		} catch (Exception E) {
			failure(testId);
			fail("No warning displayed");
		}
	}
	
	public void invalidEmailWarning(int testId) throws Exception {
		try {
			if (driver.findElement(By.cssSelector("[role^='alert']")).getText().equals("The input is not a valid e-mail")) {
				//pass
			} else {
				
				failure(testId);
				fail("Incorrect error displayed");
			}
		} catch (Exception E) {
			failure(testId);
			fail("No error displayed");
		}
	}
	
	public void editAccount(String oldName, String newName, int testId) throws Exception {
		try {
			WebElement tbl = driver.findElement(By.xpath("//table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			breakP:
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size()-1; j++) {
			    	
			    	if (cols.get(j).getText().equals(oldName) && i!=1) {	    		
			    		cols.get(2).click();
			    		found = true;
			    		break breakP;
			    	}
			    }
			}
			
			if (!found) {
				failure(testId);
				fail("Account not found");
			}
			Thread.sleep(1000);
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(newName).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys("Password1").perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys("Password1").perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	public void deleteAccount(String profile, int testId) throws Exception {
		try {
			WebElement tbl = driver.findElement(By.xpath("//table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			breakP:
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size()-1; j++) {
			    	
			    	if (cols.get(j).getText().equals(profile) && i!=1) {	    		
			    		cols.get(3).click();
			    		found = true;
			    		break breakP;
			    	}
			    }
			}
			if (!found) {
				failure(testId);
				fail("Account not found");
			}
			Thread.sleep(1000);
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	
	
	//Verifies whether profile exists
	public void findAccount(boolean expected, String profile, int testId) throws MalformedURLException, IOException, APIException {
		try {
			WebElement tbl = driver.findElement(By.xpath("//table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size()-1; j++) {
			    	if (cols.get(j).getText().equals(profile) && i!=1) {	    		
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				failure(testId);
				fail("Account not found.");
			} else if (expected != found && expected == false){
				failure(testId);
				fail("Account unexpectedly found in the list.");
			}
		} catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	//C5116
	@Test
	public void addAccountPopupTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5116);
		Thread.sleep(2000);
		obj.addAccountButton(5116);
		Thread.sleep(1000);
		obj.verifyAddAccountPopup(5116);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5116", data);
		
	}
	
	//C5113
	@Test
	public void addAccountTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5113);
		Thread.sleep(2000);
		obj.addAccount("automationtest@gmail.com","Password1","Password1", 5113);
		Thread.sleep(3000);
		obj.findAccount(true, "automationtest@gmail.com", 5113);
		Thread.sleep(1000);
		obj.deleteAccount("automationtest@gmail.com", 5113);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5113", data);
		
	}
	
	//C5120
	@Test
	public void editAccountTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5120);
		Thread.sleep(2000);
		obj.addAccount("automationtest@gmail.com","Password1","Password1", 5120);
		Thread.sleep(3000);
		obj.editAccount("automationtest@gmail.com", "automationtestEdit@gmail.com", 5120);
		Thread.sleep(1500);
		obj.findAccount(true, "automationtestEdit@gmail.com", 5120);
		obj.deleteAccount("automationtestEdit@gmail.com",5120);
		Thread.sleep(2000);
		obj.driver.navigate().refresh();
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5120", data);
		
	}
	
	//C5114
	@Test
	public void addAccountBlankDetailsTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5114);
		Thread.sleep(2000);
		obj.addAccount("","Password1","Password1", 5114);
		Thread.sleep(1000);
		obj.blankEmailWarning(5114);
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5114", data);
		
	}
	
	//C5117
	@Test
	public void addAccountInvalidPasswordTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5117);
		Thread.sleep(2000);
		obj.addAccount("automationtest@gmail.com","Password1","password1",5117);
		Thread.sleep(1000);
		obj.invalidPasswordsWarning(5117);
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5117", data);
		
	}
	
	//C5118
	@Test
	public void addAccountInvalidEmailTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5118);
		Thread.sleep(2000);
		obj.addAccount("abcd12234","Password1","Password1",5118);
		Thread.sleep(3000);
		obj.invalidEmailWarning(5118);
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5118", data);
		
	}
	//C5121
	@Test
	public void deleteAccountTest() throws Exception {
		Map data = new HashMap();
		UsersTest obj = new UsersTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.accountsScreen(5121);
		Thread.sleep(2000);
		obj.addAccount("automationtest@gmail.com","Password1","Password1",5121);
		Thread.sleep(3000);
		obj.deleteAccount("automationtest@gmail.com",5121);
		Thread.sleep(4000);
		obj.driver.navigate().refresh();
		Thread.sleep(3000);
		obj.findAccount(false, "automationtest@gmail.com",5121);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5121", data);
		
	}

}
