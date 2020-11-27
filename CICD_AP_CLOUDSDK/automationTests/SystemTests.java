package automationTests;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.internal.TextListener;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.Test;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;

public class SystemTests {
	WebDriver driver;

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
		System.setProperty("webdriver.chrome.driver", "/home/netex/nightly_sanity/ui-scripts/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--no-sandbox");
		//options.addArguments("--disable-dev-shm-usage");
		options.addArguments("--headless");
		options.addArguments("--window-size=1920,1080");
		driver = new ChromeDriver(options);
		driver.get("https://wlan-ui.qa.lab.wlan.tip.build");
	}
	
	public void closeBrowser() {
		driver.close();
	}
	
	//Log into the CloudSDK portal
	public void logIn() {
		driver.findElement(By.id("login_email")).sendKeys("support@example.com");
		driver.findElement(By.id("login_password")).sendKeys("support");
		driver.findElement(By.xpath("//*[@id=\"login\"]/button/span")).click();
	}
	
	//Navigates to systems tab
	public void systemScreen(int testId) throws Exception {
		try {
			driver.findElement(By.linkText("System")).click();
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void ouiError(int testId) throws Exception {
		try {
			Actions cursor = new Actions(driver);
			WebElement oui = driver.findElement(By.xpath("//*[@id=\"oui\"]"));
			cursor.sendKeys(oui, "abc").build().perform();
			cursor.sendKeys(Keys.ENTER).build().perform();
			Thread.sleep(1000);
			
			boolean found = false;
			if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("No matching manufacturer found for OUI")) {
				found = true;
			}
			if (!found) {
//				test.log(LogStatus.FAIL, "Error message not displayed");
			}
			Assert.assertEquals("Error message not displayed", true, found);
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void addVersion(int testId) throws Exception {
		try {
			Thread.sleep(2000);
			driver.findElement(By.xpath("//span[contains(.,'Add Version')]")).click();
			driver.findElement(By.xpath("//*[@id=\"modelId\"]")).sendKeys("TEST");
			driver.findElement(By.xpath("//*[@id=\"versionName\"]")).sendKeys("TEST");
			driver.findElement(By.xpath("//*[@id=\"filename\"]")).sendKeys("TEST");
			driver.findElement(By.xpath("//*[@id=\"validationCode\"]")).sendKeys("TEST");
			driver.findElement(By.cssSelector(".ant-btn.index-module__Button___3SCd4.ant-btn-primary")).click();
			Thread.sleep(1000);
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void addBlankVersion(int testId) throws Exception {

		try {
			driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div[2]/div[3]/button/span")).click();
			driver.findElement(By.xpath("//*[@id=\"modelId\"]")).sendKeys("TEST");	
			driver.findElement(By.xpath("//*[@id=\"filename\"]")).sendKeys("TEST");
			driver.findElement(By.xpath("//*[@id=\"validationCode\"]")).sendKeys("TEST");
			driver.findElement(By.cssSelector(".ant-btn.index-module__Button___3SCd4.ant-btn-primary")).click();
			Thread.sleep(1000);
			
			try {
				if (driver.findElement(By.cssSelector("body > div:nth-child(8) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > form > div.ant-row.ant-form-item.ant-form-item-with-help.ant-form-item-has-error > div.ant-col.ant-col-15.ant-form-item-control > div.ant-form-item-explain > div")).getText().equals("Please input your Version Name")) {
					//error message found
				} else {
					
					fail("Incorrect error message displayed");
				}
			} catch (Exception E) {
				
				fail("Error message not displayed");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void addClient(String mac, int testId) throws Exception {
		try {
			try {
				driver.findElement(By.xpath("//span[contains(.,'Add Client')]")).click();
			} catch (Exception E) {
				
				fail("Add Client button not found");
			}
		
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(mac).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
		
	}
	public void addInvalidClient(String mac, int testId) throws Exception {
		try {
			driver.findElement(By.xpath("//span[contains(.,'Add Client')]")).click();
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(mac).perform();
			Thread.sleep(500);
//			driver.findElement(By.cssSelector("body > div:nth-child(8) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > form > div > div.ant-col.ant-col-12.ant-form-item-control > div.ant-form-item-explain > div"))
//			.click();
			try {
				if (driver.findElement(By.cssSelector("body > div:nth-child(8) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > form > div > div.ant-col.ant-col-12.ant-form-item-control > div.ant-form-item-explain > div"))
						.getText().equals("Please enter a valid MAC Address.")){
					//No further steps needed
				} else {
//					System.out.print(driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-body > div:nth-child(3) > div.ant-col.ant-col-12.ant-form-item-control > div > div > div > div.ant-row.ant-form-item.ant-form-item-with-help.ant-form-item-has-error > div > div.ant-form-item-explain > div"))
//						.getText());
					
					fail("Incorrect error message displayed");
				}
			} catch (Exception E) {
				
				fail("Error message not displayed");
			}
			
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		

	}
	
	public void cancelAddClient(String mac, int testId) throws Exception {
		try {
			try {
				driver.findElement(By.xpath("//span[contains(.,'Add Client')]")).click();
			} catch (Exception E) {
				
				fail("Add Client button not found");
			}
			
			Actions browser = new Actions(driver);
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(mac).perform();
			browser.sendKeys(Keys.TAB).perform();
			browser.sendKeys(Keys.ENTER).perform();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
		
	}
	
	//Looks for the version given in the parameter and tests to see if it is the expected result
	public void findVersion(boolean expected, String version, int testId) throws MalformedURLException, IOException, APIException {
		
		try {
			WebElement tbl = driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div[2]/div[4]/div/div/div/div/div/table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size()-5; j++) {
			    	if (cols.get(j).getText().equals(version)) {
			    		
			    		//System.out.prin
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				
				fail("Version not found.");
			} else if (expected != found && expected == false){
				
				fail("Version unexpectedly found in the list.");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	//Looks for the version given in the parameter and tests to see if it is the expected result
	public void findModelTargetVersion(boolean expected, String version, int testId) throws Exception {
		try {
			Thread.sleep(2000);
			WebElement tbl = driver.findElement(By.cssSelector("#root > section > main > div:nth-child(2) > div:nth-child(2) > div > div > div > div > div > table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size()-2; j++) {
			    	if (cols.get(j).getText().equals(version)) {
			    		
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				
				fail("Version not found.");
			} else if (expected != found && expected == false){
				
				fail("Version unexpectedly found in the list.");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void findTargetEquipmentProfile(boolean expected, String profile, int testId) throws Exception {
		try {
			WebElement tbl = driver.findElement(By.xpath("//table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			//row iteration
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));
			    //column iteration
			    for(int j=0; j<cols.size()-2; j++) {
			    	
			    	if (cols.get(j).getText().equals(profile)) {
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				
				fail("Profile not found.");
			} else if (expected != found && expected == false){
				
				fail("Profile unexpectedly found in the list.");
			}
			//Assert.assertEquals(expected, found);
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void findMacAddress(boolean expected, String profile, int testId) throws Exception {
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
			    	
			    	if (cols.get(j).getText().equals(profile)) {
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				
				fail("Mac Address not found on block list.");
			} else if (expected != found && expected == false){
				
				fail("Mac Address unexpectedly found in the list.");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void createTargetEquipmentProfile(int testId) throws Exception {
		try {
			try {
				driver.findElement(By.xpath("//span[contains(.,'Add Model')]")).click();
			} catch (Exception E) {
				
				fail("Add Model button not found");
			}
			Thread.sleep(2000);
			driver.findElement(By.xpath("//input[@id='model']")).sendKeys("TEST");
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();;
			browse.sendKeys(Keys.ARROW_DOWN).perform();;
			browse.sendKeys(Keys.ENTER).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
		
	}
	
	public void editTargetButton(int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='edit-model-TEST']")).click();
			Thread.sleep(2000);
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void editTarget(String name, int testId) throws Exception {
		try {
			editTargetButton(testId);
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(name);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();
			
			//driver.findElement(By.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void testAutoProvDropdown(int testId) throws Exception {
		try {
			//String loc = driver.findElement(By.cssSelector(".ant-select-selection-item")).getAttribute("title");
			Actions browser = new Actions(driver);
			WebElement dropdown = driver.findElement(By.cssSelector(".ant-select-selection-item"));
			
			if (!dropdown.getAttribute("title").equals("Toronto")){
				
				//fail("Incorrect Locations displayed");
			}

			browser.sendKeys(dropdown, Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			
			if (!dropdown.getAttribute("title").equals("FirstFloor")){
				
				//fail("Incorrect Locations displayed");
			}
			
			browser.sendKeys(Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			
			if (!dropdown.getAttribute("title").equals("TipBuilding")){
				
				//fail("Incorrect Locations displayed");
			}
			
			browser.sendKeys(Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ARROW_DOWN).perform();
			browser.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			
			if (!dropdown.getAttribute("title").equals("Ottawa")){
				
				//fail("Incorrect Locations displayed");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void deleteTargetButton(String name, int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='delete-model-" + name + "']")).click();
			Thread.sleep(2000);
			try {
				if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle1\"]")).getText().equals("Are you sure?")){
					//No further steps needed
				} else if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle2\"]")).getText().equals("Are you sure?")){
					//Will have this Id when version edit button has been clicked prior
				} else {
					
					fail("Confirmation not found");
				}
			} catch (Exception E) {
				
				fail("Confirmation not found");
				
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void deleteTarget(String name, int testId) throws Exception {
		try {
			deleteTargetButton(name, testId);
			Thread.sleep(1000);
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			driver.navigate().refresh();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void deleteVersionButton(int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='delete-firmware-TEST']")).click();
			Thread.sleep(2000);
			try {
				if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle1\"]")).getText().equals("Are you sure?")){
					//No further steps needed
				} else if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle2\"]")).getText().equals("Are you sure?")){
					//Will have this Id when version edit button has been clicked prior
				} else {
					
					fail("Confirmation not found");
				}
			} catch (Exception E) {
				
				fail("Confirmation not found");
				
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void editVersionButton(int testId) throws Exception {
		try {
			Thread.sleep(3000);
			driver.findElement(By.cssSelector("[title^='edit-firmware-TEST']")).click();
			Thread.sleep(2000);
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void editVersion(int testId) throws Exception {
		try {
			editVersionButton(testId);
			driver.findElement(By.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/div/div/input")).sendKeys("123");
			driver.findElement(By.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	public void abortEditVersion(int testId) throws Exception {
		try {
			editVersionButton(testId);
			driver.findElement(By.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/div/div/input")).sendKeys("123");
			driver.findElement(By.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[1]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void deleteVersion(int testId) throws Exception {
		try {
			deleteVersionButton(testId);
			Thread.sleep(1000);
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			driver.navigate().refresh();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		
	}
	
	public void manufacturerScreenDetails(int testId) throws MalformedURLException, IOException, APIException {
		
		try {
			if (!driver.findElement(By.cssSelector("#root > section > main > div:nth-child(2) > div > form > div:nth-child(1) > div.ant-card-head > div > div")).getText().equals("Upload Manufacturer OUI Data")) {
				
				fail("Upload data section title incorrect");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div:nth-child(2) > div > form > div:nth-child(2) > div.ant-card-head > div > div")).getText().equals("Set a Manufacturer Alias")) {
				
				fail("Set manufacturer data section title incorrect");
			}
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail();
		}
		//Assert.assertEquals(true, found);
	}
	
	public void autoprovisionScreenDetails(boolean enabled, int testId) throws MalformedURLException, IOException, APIException {
		if (enabled) {
			try {
				if (!driver.findElement(By.cssSelector("#root > section > main > div:nth-child(2) > form > div.index-module__Content___2GmAx > div:nth-child(1) > div.ant-card-head > div > div")).getText().equals("Target Location")) {
					
					fail("Target Location title incorrect");
				} else if (!driver.findElement(By.cssSelector("#root > section > main > div:nth-child(2) > form > div.index-module__Content___2GmAx > div:nth-child(2) > div.ant-card-head > div > div.ant-card-head-title")).getText().equals("Target Equipment Profiles")) {
					
					fail("Target equipment profiles title incorrect");
				}
			} catch (Exception E) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail();
			}
		} else {
			if (driver.findElements(By.cssSelector("#root > section > main > div:nth-child(2) > form > div.index-module__Content___2GmAx > div:nth-child(1) > div.ant-card-head > div > div")).size()!=0) {
				
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail();
				
				
			}
		}	
	}
	
	public void clickSwitch() {
		driver.findElement(By.cssSelector("#enabled")).click();;
	}
	
	public void firmwareScreen(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.xpath("//*[@id=\"rc-tabs-0-tab-firmware\"]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void autoprovisionScreen(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.xpath("//*[@id=\"rc-tabs-0-tab-autoprovision\"]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void clientBListScreen(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.xpath("//*[@id=\"rc-tabs-0-tab-blockedlist\"]")).click();
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
	}
	
	public void deleteMacButton(String name, int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='delete-mac-" + name + "']")).click();
			Thread.sleep(2000);
			try {
				if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle1\"]")).getText().equals("Are you sure?")){
					//No further steps needed
				} else if (driver.findElement(By.xpath("//*[@id=\"rcDialogTitle2\"]")).getText().equals("Are you sure?")){
					//Will have this Id when version edit button has been clicked prior
				} else {
					Map data = new HashMap();
					data.put("status_id", new Integer(5));
					data.put("comment", "Fail");
					JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
					fail("Confirmation not found");
				}
			} catch (Exception E) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			}
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}

	}
	
	public void deleteMac(String name, int testId) throws Exception {
		try {
			deleteMacButton(name,testId);
			Thread.sleep(1000);
			Actions browse = new Actions(driver);
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.TAB).perform();
			browse.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1000);
			driver.navigate().refresh();
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		
		
	}
	
	//C5037
	@Test
	public void manufacturerScreenTest() throws Exception {
		Map data = new HashMap();
		
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(4000);
		obj.systemScreen(5037);
		Thread.sleep(2500);
		obj.manufacturerScreenDetails(5037);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5037", data);
		
	}
	//C5036
	@Test
	public void ouiDetailsTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5036);
		Thread.sleep(2500);
		obj.ouiError(5036);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5036", data);
		
	}
	//C5040
	@Test
	public void createVersionTest() throws Exception {
		Map data = new HashMap();
		
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5040);
		Thread.sleep(2500);
		//obj.manufacturerScreenDetails();
		obj.firmwareScreen(5040);
		Thread.sleep(1000);
		obj.addVersion(5040);
		Thread.sleep(1000);
		obj.findVersion(true, "TEST", 5040);
		Thread.sleep(2000);
		obj.deleteVersion(5040);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5040", data);
		
		
	}
	//C5038
	@Test
	public void allVersionFieldsTest() throws Exception {
		Map data = new HashMap();
		
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5038);
		Thread.sleep(2500);
		obj.firmwareScreen(5038);
		Thread.sleep(1000);
		obj.findVersion(false, "", 5038);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5038", data);
		
	}
	//C5039
	@Test
	public void modelTargetVersionFieldsTest() throws Exception {
		Map data = new HashMap();
		
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5039);
		Thread.sleep(2500);
		obj.firmwareScreen(5039);
		Thread.sleep(1000);
		obj.findModelTargetVersion(false, "", 5039);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5039", data);
		
	}
	//C5057
	@Test
	public void deleteVersionTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5057);
		Thread.sleep(2500);
		//obj.manufacturerScreenDetails();
		obj.firmwareScreen(5057);
		Thread.sleep(1000);
		obj.addVersion(5057);
		Thread.sleep(3000);
		obj.findVersion(true, "TEST", 5057);
		Thread.sleep(2000);
		obj.deleteVersion(5057);
		Thread.sleep(1000);
		obj.findVersion(false, "TEST", 5057);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5057", data);
		
	}
	//C5056
	@Test
	public void editVersionTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5056);
		Thread.sleep(2500);
		obj.firmwareScreen(5056);
		Thread.sleep(1000);
		obj.addVersion(5056);
		Thread.sleep(1000);
		obj.editVersion(5056);
		Thread.sleep(1500);
		obj.findVersion(true, "TEST123", 5056);
		obj.deleteVersion(5056);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5056", data);
		
	}
	//C5064
	@Test
	public void abortEditVersionTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5064);
		Thread.sleep(2500);
		obj.firmwareScreen(5064);
		Thread.sleep(1000);
		obj.addVersion(5064);
		Thread.sleep(1000);
		obj.abortEditVersion(5064);
		Thread.sleep(1500);
		obj.findVersion(false, "TEST123", 5064);
		obj.deleteVersion(5064);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5064", data);
		
	}
	//C5065
	@Test
	public void createBlankVersionTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5065);
		Thread.sleep(2500);
		obj.firmwareScreen(5065);
		Thread.sleep(1000);
		obj.addBlankVersion(5065);
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5065", data);
		
	}
	//C5041
	@Test
	public void autoProvEnbableSwitchTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5041);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5041);
		Thread.sleep(1000);
		obj.autoprovisionScreenDetails(true, 5041);
		obj.clickSwitch();
		Thread.sleep(1000);
		obj.autoprovisionScreenDetails(false, 5041);
		obj.clickSwitch();
		Thread.sleep(1000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5041", data);
		
	}
	
	//C5054
	@Test
	public void targetEquipmentFieldsTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5054);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5054);
		Thread.sleep(1000);
		obj.findTargetEquipmentProfile(false, "", 5054);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5054", data);
		
	}
	//C5042
	@Test
	public void createTargetEquipmentTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5042);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5042);
		Thread.sleep(1000);
		obj.createTargetEquipmentProfile(5042);
		Thread.sleep(1000);
		obj.findTargetEquipmentProfile(true, "TEST", 5042);
		obj.deleteTarget("TEST", 5042);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5042", data);
		
	}
	//C5052
	@Test
	public void deleteTargetEquipmentTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5052);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5052);
		Thread.sleep(1000);
		obj.createTargetEquipmentProfile(5052);
		Thread.sleep(1000);
		obj.deleteTarget("TEST", 5052);
		Thread.sleep(2000);
		obj.findTargetEquipmentProfile(false, "TEST", 5052);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5052", data);
		
	}
	//C5053
	@Test
	public void editTargetEquipmentTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5053);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5053);
		Thread.sleep(1000);
		obj.createTargetEquipmentProfile(5053);
		Thread.sleep(1000);
		obj.editTarget("TEST123", 5058);
		Thread.sleep(1000);
		obj.findTargetEquipmentProfile(true, "TEST123", 5053);
		obj.editTarget("TEST", 5053);
		Thread.sleep(1000);
		obj.deleteTarget("TEST", 5053);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5053", data);
		
	}
	//C5058
	@Test
	public void autoProvDropdownTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5058);
		Thread.sleep(2500);
		obj.autoprovisionScreen(5058);
		Thread.sleep(1000);
		obj.testAutoProvDropdown(5058);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5058", data);
		
	}
	
	//C5060
	@Test
	public void addClientTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5060);
		Thread.sleep(1000);
		obj.clientBListScreen(5060);
		Thread.sleep(2500);
		obj.addClient("6c:e8:5c:63:3b:5f", 5060);
		Thread.sleep(1500);
		obj.findMacAddress(true, "6c:e8:5c:63:3b:5f", 5060);
		Thread.sleep(2000);
		obj.deleteMac("6c:e8:5c:63:3b:5f", 5060);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5060", data);
		
	}
		
	//C5061
	@Test
	public void deleteClientTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5061);
		Thread.sleep(1000);
		obj.clientBListScreen(5061);
		Thread.sleep(2500);
		obj.addClient("6c:e8:5c:63:3b:5f", 5061);
		Thread.sleep(3500);
		obj.findMacAddress(true, "6c:e8:5c:63:3b:5f", 5061);
		Thread.sleep(2000);
		obj.deleteMac("6c:e8:5c:63:3b:5f", 5061);
		Thread.sleep(2000);
		obj.findMacAddress(false, "6c:e8:5c:63:3b:5f", 5061);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5061", data);
		
	}
	//C5063
	@Test
	public void cancelAddingClientTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5063);
		Thread.sleep(1000);
		obj.clientBListScreen(5063);
		Thread.sleep(2500);
		obj.cancelAddClient("6c:e8:5c:63:3b:5f", 5063);
		Thread.sleep(1500);
		obj.findMacAddress(false, "6c:e8:5c:63:3b:5f", 5063);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5063", data);
		
	}
	//C5062
	@Test
	public void addInvalidClientTest() throws Exception {
		Map data = new HashMap();
		SystemTests obj = new SystemTests();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.systemScreen(5062);
		Thread.sleep(1000);
		obj.clientBListScreen(5062);
		Thread.sleep(2500);
		obj.addInvalidClient("abc", 5062);
		Thread.sleep(1500);
		obj.findMacAddress(false, "abc", 5062);
		Thread.sleep(2000);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5062", data);
	}

}
