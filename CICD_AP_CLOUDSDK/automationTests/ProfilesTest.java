package automationTests;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.Select;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class ProfilesTest {
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
	
	//Log into the CloudSDK portal
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
	
	//Navigates to profiles tab
	public void profileScreen() throws Exception {
		driver.findElement(By.linkText("Profiles")).click();
	}
	
	public void loadAllProfiles(int testId) throws Exception {
		try {
			while (driver.findElements(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[3]/button/span")).size() != 0) {
				driver.findElement(By.xpath("/html/body/div/section/main/div/div/div[3]/button/span")).click();
				Thread.sleep(1400);	
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	//Verifies whether profile exists
	public void findProfile(boolean expected, String profile, int testId) throws Exception {
		try {
			Thread.sleep(2500);
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
			    		//System.out.prin
			    		found = true;
			    	}
			    }
			}
			if (expected != found && expected == true) {
				failure(testId);
				fail("Profile not found.");
			} else if (expected != found && expected == false){
				failure(testId);
				fail("Profile unexpectedly found in the list.");
			}
			//Assert.assertEquals(expected, found);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	
	//Verifies whether profile exists and clicks
	public void findProfile(String profile, int testId) throws MalformedURLException, IOException, APIException {
		try {
			WebElement tbl = driver.findElement(By.xpath("//table"));
			List<WebElement> rows = tbl.findElements(By.tagName("tr"));
			boolean found = false;
			breakP:
			//row iteration
			for(int i=0; i<rows.size(); i++) {
			    //check column each in row, identification with 'td' tag
			    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

			    //column iteration
			    for(int j=0; j<cols.size(); j++) {
			    	if (cols.get(j).getText().equals(profile)) {
			    		cols.get(j).click();
			    		found = true;
			    		break breakP;
			    	}
			    }
			}
			if (!found) {
				failure(testId);
				fail("Profile not found.");
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}
	}
	
	public void verifyProfile(String profile, int testId) throws MalformedURLException, IOException, APIException {
		try {
			if (driver.findElement(By.cssSelector(".ant-form > .ant-card .ant-card-head-title")).getText().equals("Edit "+ profile)) {
				//Correct profile
			}
			else {
				failure(testId);
				fail("Incorrect Profile selected");
			}
		} catch (Exception E) {
			failure(testId);
			fail("No title found for profile");
		}
	}
	
	public void deleteProfileButton(int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='delete-AutomationTest Profile']")).click();
			Thread.sleep(2000);
			
			if (driver.findElement(By.cssSelector(".ant-modal-title")).getText().equals("Are you sure?")){
				//No further steps needed
			} else {
				
				fail("Popup displays incorrect text");
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
		
	}
	
	public void deleteProfile(int testId) throws Exception {
		try {
			deleteProfileButton(testId);
			Thread.sleep(1000);
			driver.findElement(By.cssSelector(".ant-btn.index-module__Button___3SCd4.ant-btn-danger")).click();
			Thread.sleep(1000);
			driver.navigate().refresh();
			Thread.sleep(3000);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void cancelDeleteProfile(int testId) throws Exception {
		try {
			deleteProfileButton(testId);
			Thread.sleep(1000);
			driver.findElement(By.cssSelector("body > div:nth-child(9) > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-footer > div > button:nth-child(1) > span")).click();
			Thread.sleep(1000);
			driver.navigate().refresh();
			Thread.sleep(1500);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	//Clicks add profile button
	public void addProfileButton(int testId) throws Exception {
		try {
			driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[1]/div/a/button/span")).click();
			Thread.sleep(1000);
			String URL = driver.getCurrentUrl();
			Assert.assertEquals("Incorrect URL", URL, "https://wlan-ui.qa.lab.wlan.tip.build/addprofile");
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	//Clicks refresh button
	public void refreshButton(int testId) throws Exception {
		try {
			//Select SSID from the drop-down
			driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[1]/div/button")).click();
			Thread.sleep(1000);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void refreshNotification(int testId) throws MalformedURLException, IOException, APIException {
		
		try {
			if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Profiles reloaded")) {
				//pass
			}
		} catch (Exception E) {
			failure(testId);
			fail("Notification not found");
		}
		
		
	}
	
	public void ssidDetails(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.xpath("//*[@id=\"name\"]")).sendKeys("AutomationTest Profile");
			driver.findElement(By.xpath("//*[@id=\"ssid\"]")).sendKeys("Automation Test SSID");
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void saveProfile(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div/div/button/span")).click();
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void abortCreatingProfile(int testId) throws Exception {
		try {
			driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div/button/span[2]")).click();
			Thread.sleep(1000);
			driver.findElement(By.cssSelector("body > div:nth-child(9) > div > div.ant-modal-wrap > div > div.ant-modal-content > "
					+ "div.ant-modal-footer > div > button.ant-btn.index-module__Button___3SCd4.ant-btn-primary")).click();
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void useCaptivePortal(int testId) throws Exception {
		try {
			driver.findElement(By.xpath("//*[@id=\"captivePortal\"]/label[2]/span[1]/input")).click();
			Thread.sleep(1000);
			
			if (driver.findElements(By.xpath("//*[@id=\"captivePortalId\"]")).size()>0) {
				//successfully found drop-down
			} else {
				
				fail("No options for captive portal found");
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void ssidList(int testId) throws Exception {
		try {
			//System.out.print(driver.findElements(By.className("ant-select-selection-search-input")).size());
			Actions cursor = new Actions(driver);
			WebElement input = driver.findElement(By.cssSelector("#rc_select_1"));
			cursor.click(input);
			cursor.sendKeys(input, "EA8300_5G_WPA2").perform();
			cursor.sendKeys(input, Keys.ENTER).perform();
			Thread.sleep(3000);
			
			if (driver.findElements(By.className("ant-table-empty")).size()!=0) {
				failure(testId);
				fail("Table not displaying SSIDs");
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}

		
	}
	
	public void bandwidthDetails(int testId) throws Exception {
		try {
			WebElement bandwidth = driver.findElement(By.xpath("//*[@id=\"bandwidthLimitDown\"]"));
			//Actions action = new Actions(driver);
			bandwidth.sendKeys(Keys.BACK_SPACE);
			bandwidth.sendKeys("123");
			Thread.sleep(500);
			
			try {
				if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-body > div:nth-child(3) > div.ant-col.ant-col-12.ant-form-item-control > div > div > div > div.ant-row.ant-form-item.ant-form-item-with-help.ant-form-item-has-error > div > div.ant-form-item-explain > div"))
						.getText().equals("Downstream bandwidth limit can be a number between 0 and 100.")){
					failure(testId);
					fail();
				}
			} catch (Exception E) {
				failure(testId);
				fail();
			}

			bandwidth.sendKeys(Keys.BACK_SPACE);
			bandwidth.sendKeys(Keys.BACK_SPACE);
			bandwidth.sendKeys(Keys.BACK_SPACE);
			
			bandwidth.sendKeys("-10");
			Thread.sleep(500);
			
			
			try {
				if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-body > div:nth-child(3) > div.ant-col.ant-col-12.ant-form-item-control > div > div > div > div.ant-row.ant-form-item.ant-form-item-with-help.ant-form-item-has-error > div > div.ant-form-item-explain > div"))
						.getText().equals("Downstream bandwidth limit can be a number between 0 and 100.")){
					failure(testId);
					fail();
				}
			} catch (Exception E) {
				failure(testId);
				fail();
				
			}
			
			bandwidth.sendKeys(Keys.BACK_SPACE);
			bandwidth.sendKeys(Keys.BACK_SPACE);
			bandwidth.sendKeys(Keys.BACK_SPACE);
			
			bandwidth.sendKeys("10");
			Thread.sleep(500);
			
			
			if (driver.findElements(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-body > div:nth-child(3) > div.ant-col.ant-col-12.ant-form-item-control > div > div > div > div.ant-row.ant-form-item.ant-form-item-with-help.ant-form-item-has-error > div > div.ant-form-item-explain > div"))
					.size()!=0){
				failure(testId);
				fail();
				
			}
		} catch (Exception E) {
			failure(testId);
			fail();
		}

			
	}
	
	public void selectSSID(int testId) throws Exception {
		try {
			Actions cursor = new Actions(driver);
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.ENTER).perform();
			cursor.sendKeys(Keys.ENTER).perform();

			Thread.sleep(1000);
			
			boolean found = true;
			try {
				if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-head > div > div")).getText().equals("SSID")) {
					found = false;
				} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(2) > div.ant-card-head > div > div")).getText().equals("Network Connectivity")) {
					found = false;
				} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(3) > div.ant-card-head > div > div")).getText().equals("Security and Encryption")) {
					found = false;
				} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(4) > div.ant-card-head > div > div")).getText().equals("Roaming")) {
					found = false;
				}
			} catch (Exception E) {
				failure(testId);
				fail();
				
			}
			Assert.assertEquals(true, found);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	
	public void selectAP(int testId) throws Exception {
		try {
			Actions cursor = new Actions(driver);
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.ENTER).perform();
			cursor.sendKeys(Keys.ARROW_DOWN).perform();
			cursor.sendKeys(Keys.ENTER).perform();
			Thread.sleep(1500);

			try {
				if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(1) > div.ant-card-head > div > div")).getText().equals("LAN and Services")) {
					failure(testId);
					fail();
				} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > form > div.index-module__ProfilePage___OaO8O > div:nth-child(2) > div.ant-card-head > div > div")).getText().equals("Wireless Networks (SSIDs) Enabled on This Profile")) {
					failure(testId);
					fail();
				}
			} catch (Exception E) {
				failure(testId);
				fail();
			}
			

			//Assert.assertEquals(true, found);
		} catch (Exception E) {
			failure(testId);
			fail();
		}
		
	}
	//C4807	
	@Test
	public void addProfileButtonTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4807);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4807", data);
	}
	
	//C4808
	@Test
	public void ssidOptionsVerificationTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4808);
		Thread.sleep(1000);
		obj.selectSSID(4088);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4808", data);
	}
	
	//C4809
	@Test
	public void apOptionsVerificationTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4809);
		Thread.sleep(1000);
		obj.selectAP(4809);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4809", data);
		
	}
	//C4824
	@Test
	public void refreshButtonTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.refreshButton(4824);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4824", data);
		
	}
	//C4818
	@Test
	public void bandwidthTest() throws Exception {
		Map data = new HashMap();
		
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4818);
		Thread.sleep(1000);
		obj.selectSSID(4818);
		obj.ssidDetails(4818);
		obj.bandwidthDetails(4818);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4818", data);
		
	}
	
	//C4819
	@Test
	public void captivePortalDropdownTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4819);
		Thread.sleep(1000);
		obj.selectSSID(4819);
		obj.ssidDetails(4819);
		obj.useCaptivePortal(4819);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4819", data);
	}
	
	//C4822
	@Test
	public void ssidListTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4822);
		Thread.sleep(1000);
		obj.selectAP(4822);
		Thread.sleep(500);
		obj.ssidList(4822);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4822", data);
	}
	//C4810
	@Test
	public void createProfileTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4810);
		Thread.sleep(600);
		obj.selectSSID(4810);
		obj.ssidDetails(4810);
		obj.saveProfile(4810);
		Thread.sleep(1000);
		obj.loadAllProfiles(4810);
		obj.findProfile(true, "AutomationTest Profile",4810);
		obj.deleteProfile(4810);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4810", data);
	}
	//C4811
	@Test
	public void profileNotCreatedTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4811);
		Thread.sleep(600);
		obj.selectSSID(4811);
		obj.ssidDetails(4811);
		obj.abortCreatingProfile(4811);
		Thread.sleep(1000);
		obj.loadAllProfiles(4811);
		obj.findProfile(false, "AutomationTest Profile",4811);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4811", data);
	}
	//C4814	
	@Test
	public void deleteProfileTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4814);
		Thread.sleep(600);
		obj.selectSSID(4814);
		obj.ssidDetails(4814);
		obj.saveProfile(4814);
		Thread.sleep(1000);
		obj.loadAllProfiles(4814);
		Thread.sleep(1000);
		obj.findProfile(true, "AutomationTest Profile",4814);
		obj.deleteProfile(4814);
		obj.loadAllProfiles(4814);
		Thread.sleep(1500);
		obj.findProfile(false, "AutomationTest Profile",4814);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4814", data);
	}
	
	//C4813	
	@Test
	public void cancelDeleteProfileTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4813);
		Thread.sleep(600);
		obj.selectSSID(4813);
		obj.ssidDetails(4813);
		obj.saveProfile(4813);
		Thread.sleep(1000);
		obj.loadAllProfiles(4813);
		obj.findProfile(true, "AutomationTest Profile", 4813);
		obj.cancelDeleteProfile(4813);
		Thread.sleep(1500);
		obj.loadAllProfiles(4813);
		obj.findProfile(true, "AutomationTest Profile",4813);
		//Delete profile at the end of the test
		obj.deleteProfile(4813);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4813", data);
	}
	//C4812	
	@Test
	public void verifyDeleteConfirmationTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.addProfileButton(4812);
		Thread.sleep(600);
		obj.selectSSID(4812);
		obj.ssidDetails(4812);
		obj.saveProfile(4812);
		Thread.sleep(2000);
		obj.loadAllProfiles(4812);
		obj.findProfile(true, "AutomationTest Profile",4812);
		obj.deleteProfileButton(4812);
		obj.driver.navigate().refresh();
		Thread.sleep(2000);
		obj.loadAllProfiles(4812);
		obj.findProfile(true, "AutomationTest Profile",4812);
		//Delete profile at the end of the test
		obj.deleteProfile(4812);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4812", data);
	}
	//C4815	
	@Test
	public void viewProfileTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.findProfile("ECW5410 Automation",4815);
		Thread.sleep(5000);
		obj.verifyProfile("ECW5410 Automation",4815);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/4815", data);
	}
	//C5035
	@Test
	public void verifyFieldsTest() throws Exception {
		Map data = new HashMap();
		ProfilesTest obj = new ProfilesTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.profileScreen();
		Thread.sleep(2500);
		obj.loadAllProfiles(5035);
		obj.findProfile(false, "",5035);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5035", data);
	}
}
