package automationTests;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.Test;
import org.junit.internal.TextListener;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class LoginTest {
	
	WebDriver driver, driver2;
	static APIClient client;
	static long runId;
	
	@BeforeClass
	public static void startTest() throws Exception
	{
		client = new APIClient("https://telecominfraproject.testrail.com");
		client.setUser("syama.devi@connectus.ai");
		client.setPassword("Connectus123$");
		
		JSONArray c = (JSONArray) client.sendGet("get_runs/5");
		runId = new Long(0);
		Calendar cal = Calendar.getInstance();
		//Months are indexed 0-11 so add 1 for current month
		int month = cal.get(Calendar.MONTH) + 1;
		String date = "UI Automation Run - " + cal.get(Calendar.DATE) + "/" + month + "/" + cal.get(Calendar.YEAR);
		
		for (int a = 0; a < c.size(); a++) {
			if (((JSONObject) c.get(a)).get("name").equals(date)) {
				runId =  (Long) ((JSONObject) c.get(a)).get("id"); 
			}
		}
	}

	public void launchBrowser() {
		System.setProperty("webdriver.chrome.driver", "/Users/mohammadrahman/Downloads/chromedriver");
//		System.setProperty("webdriver.chrome.driver", "/Users/mohammadrahman/Downloads/chromedriver");System.setProperty("webdriver.chrome.driver", "/home/netex/nightly_sanity/ui-scripts/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--no-sandbox");
//		options.addArguments("--disable-dev-shm-usage");
		options.addArguments("--headless");
		options.addArguments("--window-size=1920,1080");
		driver = new ChromeDriver(options);
		driver.get("https://wlan-ui.qa.lab.wlan.tip.build");
		
	}
	
	public void launchPortal() {
		driver2 = new ChromeDriver();
		driver2.get("https://wlan-ui.qa.lab.wlan.tip.build/");
	}
	
	public void launchSecondWindow() throws Exception {
		Actions action = new Actions(driver);
	    String URL = driver.getCurrentUrl();
	    action.sendKeys(Keys.chord(Keys.CONTROL, "n")).build().perform();
		driver.get(URL);
		Thread.sleep(2000);
	}
	
	public void login(String email, String password) {
		driver.findElement(By.id("login_email")).sendKeys(email);
		driver.findElement(By.id("login_password")).sendKeys(password);
		driver.findElement(By.xpath("//*[@id=\"login\"]/button/span")).click();	
	}
	
	public void checkHover(String box, int testId) throws Exception {
		try {
			String colour, colour2;
			if (box.equals("confirm")) {
				colour = driver.findElement(By.cssSelector("#login > button")).getCssValue("background-color");
				WebElement button = driver.findElement(By.cssSelector("#login > button"));
				
				Actions mouse = new Actions(driver);
				mouse.moveToElement(button).perform();
				Thread.sleep(500);
				
				colour2 = driver.findElement(By.cssSelector("#login > button")).getCssValue("background-color");
				
			} else if (box.equals("email")) {
				colour = driver.findElement(By.cssSelector("#login_email")).getCssValue("border-color");
				WebElement button = driver.findElement(By.cssSelector("#login_email"));		
				
				Actions mouse = new Actions(driver);
				mouse.moveToElement(button).perform();
				Thread.sleep(500);
				
				colour2 = driver.findElement(By.cssSelector("#login_email")).getCssValue("border-color");
				
			} else {		
				colour = driver.findElement(By.cssSelector("#login_password")).getCssValue("background-color");
				WebElement button = driver.findElement(By.cssSelector("#login_password"));
				
				Actions mouse = new Actions(driver);
				mouse.moveToElement(button).perform();
				Thread.sleep(500);
				
				colour2 = driver.findElement(By.cssSelector("#login_password")).getCssValue("background-color");
			}
			if (colour.equals(colour2)) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("failure");
				//Assert.assertNotEquals("Colours did not change when in focus", colour, colour2);
				
			}
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
		
		
	}
	
	public void checkEmailFocus(int testId) throws Exception {
		try {
			WebElement email= driver.findElement(By.id("login_email"));
			boolean emailFocus = email.equals(driver.switchTo().activeElement());
			if (!emailFocus) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("Email field is not in focus", true, emailFocus);
		} catch (Exception E){
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
		
	}
	
	public void checkTab(int testId) throws Exception {
		try {
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			Thread.sleep(1000);
			WebElement email= driver.findElement(By.id("login_email"));
//			System.out.print(driver.switchTo().activeElement());
			boolean emailFocus = email.equals(driver.switchTo().activeElement());
			
			if (!emailFocus) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			
			Assert.assertEquals("Email field is not in focus",true, emailFocus);
			
			browse.sendKeys(Keys.TAB).perform();
			Thread.sleep(1000);
			WebElement password= driver.findElement(By.id("login_password"));
			boolean passwordFocus = password.equals(driver.switchTo().activeElement());
			
			if (!passwordFocus) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("Password field is not in focus",true, passwordFocus);
			
			browse.sendKeys(Keys.TAB).perform();
			Thread.sleep(1000);
			WebElement confirm= driver.findElement(By.cssSelector("#login > button"));
			boolean confirmFocus = confirm.equals(driver.switchTo().activeElement());
			
			if (!confirmFocus) {
				
			}
			Assert.assertEquals("Login button is not in focus", true, confirmFocus);
		}catch (Exception E){
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void coverPassword(String password, int testId) throws Exception {
		try {
			driver.findElement(By.id("login_password")).sendKeys(password);
			
			WebElement passwordCovered = driver.findElement(By.id("login_password"));
			boolean passwordTest = (passwordCovered.getAttribute("type").equals("password"));
			if (!passwordTest) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("Password is uncovered", true, passwordTest);
			Thread.sleep(1500);
			
			driver.findElement(By.cssSelector("#login > div.ant-row.ant-form-item.ant-form-item-has-success > div.ant-col.ant-col-15.ant-form-item-control > div > div > span > span > span > svg")).click();;
			Thread.sleep(1500);
			
			WebElement passwordUncovered = driver.findElement(By.id("login_password"));
			boolean passwordTest2 = (passwordCovered.getAttribute("type").equals("text")); 
			if (!passwordTest2) {
				
			}
			Assert.assertEquals("Password is still hidden", true, passwordTest2);
		} catch (Exception E){
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
			
	}
	
	public void copyPassword(String password, int testId) throws Exception {
		try {
			driver.findElement(By.id("login_password")).sendKeys(password);
			
			WebElement passwordCovered = driver.findElement(By.id("login_password"));
			
	        WebElement locOfOrder = driver.findElement(By.id("login_password"));
			Actions act = new Actions(driver);
			act.moveToElement(locOfOrder).doubleClick().build().perform();
			
			driver.findElement(By.id("login_password")).sendKeys(Keys.chord(Keys.CONTROL,"c"));
			// now apply the command to paste
			driver.findElement (By.id("login_email")).sendKeys(Keys.chord(Keys.CONTROL, "v"));
			
			//Assert.assertEquals(expected, actual);
		} catch (Exception E){
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void logout(int testId) throws Exception {
		driver.findElement(By.cssSelector(".anticon-setting > svg")).click();
		Thread.sleep(2500);
		driver.findElement(By.linkText("Log Out")).click();
		
	}
	public void loginEnter(String email, String password, int testId) {
		driver.findElement(By.id("login_email")).sendKeys(email);
		driver.findElement(By.id("login_password")).sendKeys(password);
		driver.findElement(By.id("login_password")).sendKeys(Keys.ENTER);
		//driver.sendKeys(Keys.RETURN);	
	}
	public void backButton() {
		driver.navigate().back();	
	}
	
	public void loginBlank(int testId) {
		driver.findElement(By.xpath("//*[@id=\"login\"]/button/span")).click();	
	}
	
	public void errorNotification(int testId) throws Exception {
		try {
			boolean found = false;
			if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Invalid e-mail or password.")) {
				found = true;
			}
			if (!found) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("No error message displayed", true, found);
		} catch (Exception E){
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void emailField(int testId) throws Exception {
		try {
			if (!driver.findElement(By.id("login_email")).isDisplayed()) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("Email field not found", true, driver.findElement(By.id("login_email")).isDisplayed());
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
		
	}
	
	public void passwordField(int testId) throws Exception {
		try {
			if (!driver.findElement(By.id("login_password")).isDisplayed()) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Password field not found");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
			Assert.assertEquals("Password field not found", true, driver.findElement(By.id("login_password")).isDisplayed());
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void verifyLoginPass(int testId) throws Exception {
		try {
			String URL = driver.getCurrentUrl();
			if (!URL.equals("https://wlan-ui.qa.lab.wlan.tip.build/dashboard")) {
				
			}
			Assert.assertEquals("Incorrect URL", URL, "https://wlan-ui.qa.lab.wlan.tip.build/dashboard");
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void verifyLoginFail(int testId) throws Exception {
		try {
			String URL = driver.getCurrentUrl();
			if (!URL.equals("https://wlan-ui.qa.lab.wlan.tip.build/login")) {
				
			}
			Assert.assertEquals("Incorrect URL", URL, "https://wlan-ui.qa.lab.wlan.tip.build/login");
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void closeBrowser() {
		driver.close();
	}
	
	
	//C4099, C4164, C4172
	@Test
	public void loginTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support");
		Thread.sleep(3000);
		obj.verifyLoginPass(4099);
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4099", data);
		JSONObject t = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4164", data);
		JSONObject s = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4172", data);
		
	}
	
	//C4097
	@Test
	public void verifyEmailFieldTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.emailField(4097);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4097", data);
		
	}

	//C4098
	@Test
	public void verifyPasswordFieldTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.passwordField(4098);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4098", data);
		
	}
	
	//C4157
	@Test
	public void loginTestUppercase() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("SUPPORT@EXAMPLE.COM", "support");
		Thread.sleep(3000);
		obj.verifyLoginPass(4157);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4157", data);
		
	}
	
	//C4166
	@Test
	public void loginTestPasswordFail() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support1");
		Thread.sleep(3000);
		obj.verifyLoginFail(4166);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4166", data);
		
	}
	
	//C4167
	@Test
	public void loginTestEmailFail() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support1@example.com", "support");
		Thread.sleep(3000);
		obj.verifyLoginFail(4167);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4167", data);
		
	}
	
	//C4165
	@Test
	public void loginTestEmailPasswordFail() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support1@example.com", "support1");
		Thread.sleep(3000);
		obj.verifyLoginFail(4165);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4165", data);
		
	}
	//C4168
	@Test
	public void loginTestBlankFail() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.loginBlank(4168);
		Thread.sleep(3000);
		obj.verifyLoginFail(4168);
		Thread.sleep(1000);
		obj.closeBrowser();
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4168", data);
		
	}
	//C4163
	@Test
	public void loginEnterKeyTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.loginEnter("support@example.com", "support", 4163);
		Thread.sleep(3000);
		obj.verifyLoginPass(4163);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4163", data);
		
	}
	//C4169
	@Test
	public void loginBackButtonTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support");
		Thread.sleep(3000);
		obj.verifyLoginPass(4169);
		obj.backButton();
		Thread.sleep(3000);
		obj.verifyLoginPass(4169);
		Thread.sleep(1500);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4169", data);
		
	}
	//C4171
	@Test
	public void logoutTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support");
		Thread.sleep(3000);
		obj.verifyLoginPass(4171);
		obj.logout(4171);
		Thread.sleep(3000);
		obj.verifyLoginFail(4171);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4171", data);
		
	}
	
	//C4160
	@Test
	public void logoutBackButtonTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support");
		Thread.sleep(3000);
		obj.verifyLoginPass(4160);
		obj.logout(4160);
		Thread.sleep(3000);
		obj.backButton();
		Thread.sleep(2000);
		obj.verifyLoginFail(4160);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4160", data);
	}
	
	///C4103
	@Test
	public void showPasswordTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.coverPassword("support", 4103);
		Thread.sleep(3000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4103", data);
	}
	
	//C4105
	@Test
	public void errorNotificationTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.login("support@example.com", "support1");
		Thread.sleep(2000);
		obj.errorNotification(4105);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4105", data);
	}
	//C4162
	@Test
	public void tabFunctionalityTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(3000);
		obj.checkTab(4162);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4162", data);
	}
	//C4100
	@Test
	public void hoverLoginButtonTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(3000);
		obj.checkHover("confirm", 4100);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4100", data);
	}
	//C4101
	@Test
	public void hoverEmailFieldTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(3000);
		obj.checkHover("email", 4101);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4101", data);
	}
	//C4102
	@Test
	public void hoverPwdFieldTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(3000);
		obj.checkHover("password", 4102);
		Thread.sleep(1000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4102", data);
	}
//	@Test
//	public void stayLoggedInTest() throws Exception {
//		Map data = new HashMap();
//		LoginTest obj = new LoginTest();
//		obj.launchBrowser();
//		Thread.sleep(2000);
//		obj.login("support@example.com", "support");
//		Thread.sleep(3000);
//		obj.verifyLoginPass();
//		Thread.sleep(1000);
//		obj.closeBrowser();
//		Thread.sleep(2000);
//		obj.launchPortal();
//		Thread.sleep(2500);
//		obj.launchSecondWindow();
//		obj.closeBrowser();
//		data.put("status_id", new Integer(1));
//		data.put("comment", "This test worked fine!");
//		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/812/5036", data);
//	}
//	@Test
//	public void newBrowserTest() throws Exception {
//		Map data = new HashMap();
//		LoginTest obj = new LoginTest();
//		obj.launchBrowser();
//		Thread.sleep(2000);
//		obj.login("support@example.com", "support");
//		Thread.sleep(3000);
//		obj.verifyLoginPass();
//		Thread.sleep(1000);
//		obj.launchPortal();
//		obj.verifyLoginPass();
//		obj.closeBrowser();
//		data.put("status_id", new Integer(1));
//		data.put("comment", "This test worked fine!");
//		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/812/5036", data);
//	}
	
	//C4159
	@Test
	public void copyPasswordTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.copyPassword("support", 4159);
		Thread.sleep(3000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4159", data);
	}
	//C4161
	@Test
	public void initialFocusTest() throws Exception {
		Map data = new HashMap();
		LoginTest obj = new LoginTest();
		obj.launchBrowser();
		Thread.sleep(2000);
		obj.checkEmailFocus(4161);
		Thread.sleep(3000);
		obj.closeBrowser();
		
		System.out.print("passed");
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4161", data);
	}
}
