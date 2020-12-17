package automationTests;

import static org.junit.jupiter.api.Assertions.fail;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;


public class NetworkTest {
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
//		System.setProperty("webdriver.chrome.driver", "/Users/mohammadrahman/Downloads/chromedriver");
		System.setProperty("webdriver.chrome.driver", "/home/netex/nightly_sanity/ui-scripts/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--no-sandbox");
		options.addArguments("--headless");
		options.addArguments("--window-size=1920,1080");
		driver = new ChromeDriver(options);
		driver.get("https://wlan-ui.qa.lab.wlan.tip.build");	
	}
	
	public void failure(int testId) throws MalformedURLException, IOException, APIException {
		driver.close();
		Map data = new HashMap();
		data.put("status_id", new Integer(5));
		data.put("comment", "Fail");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
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
	
	public void networkScreen(int testId) throws Exception {
		try {
			driver.findElement(By.linkText("Network")).click();
		}catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
		
	public void loadAllProfiles(int testId) throws Exception {
		try {
			while (driver.findElements(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[3]/button/span")).size() != 0) {
				driver.findElement(By.xpath("/html/body/div/section/main/div/div/div[3]/button/span")).click();
				Thread.sleep(2000);	
			}
		}catch (Exception E) {
			failure(testId);
			fail("Fail");
		}
		
	}
	
	public void addLocation(String loc, int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector(".ant-tree-node-content-wrapper:nth-child(3) > .ant-tree-title > span")).click();
		} catch (Exception E) {
			failure(testId);
			
			fail("Locations not found");
		}
		
		Thread.sleep(1000);
		
		try {
			driver.findElement(By.xpath("//span[contains(.,'Add Location')]")).click();
		} catch (Exception E) {
			failure(testId);
			
			fail("Add location button not found");
		}
		Thread.sleep(1000);
		Actions browser = new Actions(driver);
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(loc).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.ENTER).perform();
		Thread.sleep(2000);
		
		if (!driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).getText().equals(loc)) {
			failure(testId);
			fail("Fail");
		}
	}
	
	public void deleteLocation(String loc, int testId) throws Exception {
		driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).click();
		Thread.sleep(1000);
		driver.findElement(By.xpath("//span[contains(.,'Delete Location')]")).click();
		Thread.sleep(2000);
		if (!driver.findElement(By.cssSelector(".ant-modal-body > p > i")).getText().equals(loc)) {
			failure(testId);
			fail("Location not deleted");
		}
		Actions browser = new Actions(driver);
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.ENTER).perform();
		Thread.sleep(2000);
	}
		
	//Verifies no field is blank in the column
	public void verifyNetworkFields(boolean expected, String profile, int column, int testId) throws MalformedURLException, IOException, APIException {
		WebElement tbl = driver.findElement(By.xpath("//table"));
		List<WebElement> rows = tbl.findElements(By.tagName("tr"));
		
		//row iteration
		for(int i=2; i<rows.size(); i++) {
		    //check column each in row, identification with 'td' tag
		    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));
		    System.out.print(cols.get(column).getText());
	    	if (cols.get(column).getText().equals(profile) && !expected) {
		    	Map data = new HashMap();
		    	data.put("status_id", new Integer(5));
		   		data.put("comment", "Fail");
		 		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		  		fail("Fail");
	    	}
		}
	}
	
	//Verifies whether profile exists and clicks
	public void findNetwork(String profile, int testId) throws MalformedURLException, IOException, APIException {
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
		    		found  = true;
		    		break breakP;
		    	}
		    }
		}
		
		if (!found) {
			failure(testId);
			fail("Network not found");
		}
		//Assert.assertEquals(false, found);
	}
	
	public void verifyDevice(String profile, int testId) throws MalformedURLException, IOException, APIException {
		try {
			if (driver.findElement(By.cssSelector(".index-module__DeviceDetailCard___2CFDA.ant-card-bordered > div > div > div.index-module__leftWrapContent___2iZZo > p:nth-child(1)")).getText().equals(profile)) {
				//Pass
			}
			else {
				//System.out.print(driver.findElement(By.cssSelector(".index-module__DeviceDetailCard___2CFDA.ant-card-bordered > div > div > div.index-module__leftWrapContent___2iZZo > p:nth-child(1)")).getText());
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Wrong profile");
			}
		} catch (Exception E) {
			failure(testId);
			fail("Profile title not found");
		}
	}
	
	
	public void verifyAP(String profile, int testId) throws MalformedURLException, IOException, APIException {
		try {
			if (driver.findElement(By.cssSelector("#root > section > main > div > div > div.index-module__mainContent___1X1X6 > div > div.ant-card.ant-card-bordered.ant-card-contain-tabs > div.ant-card-head > div.ant-card-head-wrapper > div.ant-card-head-title > div > div > div:nth-child(1)")).getText().equals(profile)) {
				//Correct profile
			}
			else {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Fail");
			}
		} catch (Exception E) {
			failure(testId);
			fail("Profile title not found");
		}
	}
	
	
	public void verifyAPLocation(int testId) throws MalformedURLException, IOException, APIException {
		try {
			String location = driver.findElement(By.cssSelector(".ant-breadcrumb-link")).getText();
			
			driver.findElement(By.cssSelector("[id^='rc-tabs-0-tab-location']")).click();
			Thread.sleep(2000);
			String dropdownVerification = "[title^='"+location+"']";
			if (driver.findElements(By.cssSelector(dropdownVerification)).size()==0) {
				Map data = new HashMap();
				data.put("status_id", new Integer(5));
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Wrong location");
			}
			
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail("Profile title not found");
		}
	}
	
	public void refreshButton(int testId) throws Exception {
		try {
			driver.findElement(By.cssSelector("[title^='reload']")).click();
		} catch (Exception E) {
			failure(testId);
			fail ("Reload button not visible");
		}
		
		Thread.sleep(1000);
	}
	
	
	public void clientBlockedListButton(int testId) throws Exception {
		driver.findElement(By.xpath("//span[contains(.,'Blocked List')]")).click();
		Thread.sleep(2000);
		String URL = driver.getCurrentUrl();
		
		if (!URL.equals("https://wlan-ui.qa.lab.wlan.tip.build/system/blockedlist")) {
			failure(testId);
			
			fail ();
		}
		//Assert.assertEquals(URL, "https://portal.dev1.netexperience.com/configure/system/blockedlist");
		
	}
		
	public void refreshNotificationAP(int testId) throws MalformedURLException, IOException, APIException {
		
		if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Access points reloaded.")) {
			
		} else {
			failure(testId);
			fail("Notification did not appear");
		}
	}
	public void refreshNotificationClientDevice(int testId) throws MalformedURLException, IOException, APIException {
		if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Client devices reloaded.")) {
			
		} else {
			failure(testId);
			fail("Notification did not appear");
		}
	}
	
	public void clientDevicesScreen(int testId) throws MalformedURLException, IOException, APIException {
		try {
			driver.findElement(By.linkText("Client Devices")).click();
		} catch (Exception E) {
			failure(testId);
			fail("Client Devices tab not visible");
		}
		
	}
	
	//C5603
	@Test
	public void verifyNameFields() throws Exception {
		int testId = 5603;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 0, testId);
		obj.verifyNetworkFields(false, "N/A", 0, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5604
	@Test
	public void verifyAlarmFields() throws Exception {
		int testId = 5604;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 1, testId);
		obj.verifyNetworkFields(false, "N/A", 1, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5605
	@Test
	public void verifyModelField() throws Exception {
		int testId = 5605;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 2, testId);
		obj.verifyNetworkFields(false, "N/A", 2, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5606
	@Test
	public void verifyIPField() throws Exception {
		int testId = 5606;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 3, testId);
		obj.verifyNetworkFields(false, "N/A", 3, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5607
	@Test
	public void verifyMACField() throws Exception {
		int testId = 5607;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 4, testId);
		obj.verifyNetworkFields(false, "N/A", 4, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5608
	@Test
	public void verifyManufacturerField() throws Exception {
		int testId = 5608;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 5, testId);
		obj.verifyNetworkFields(false, "N/A", 5, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5609
	@Test
	public void verifyFirmwareField() throws Exception {
		int testId = 5609;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 6, testId);
		obj.verifyNetworkFields(false, "N/A", 6, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5610
	@Test
	public void verifyAssetIdField() throws Exception {
		int testId = 5610;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 7, testId);
		obj.verifyNetworkFields(false, "N/A", 7, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5611
	@Test
	public void verifyUpTimeField() throws Exception {
		int testId = 5611;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 8, testId);
		obj.verifyNetworkFields(false, "N/A", 8, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5612
	@Test
	public void verifyProfileField() throws Exception {
		int testId = 5612;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 9, testId);
		obj.verifyNetworkFields(false, "N/A", 9, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5613
	@Test
	public void verifyChannelField() throws Exception {
		int testId = 5613;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 10, testId);
		obj.verifyNetworkFields(false, "N/A", 10, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5614
	@Test
	public void verifyOccupancyField() throws Exception {
		int testId = 5614;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 11, testId);
		obj.verifyNetworkFields(false, "N/A", 11, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5615
	@Test
	public void verifyNoiseFloorField() throws Exception {
		int testId = 5615;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 12, testId);
		obj.verifyNetworkFields(false, "N/A", 12, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5616
	@Test
	public void verifyDevicesField() throws Exception {
		int testId = 5616;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(testId);
		Thread.sleep(5000);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 13, testId);
		obj.verifyNetworkFields(false, "N/A", 13, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/" + testId, data);
	}
	
	//C5618
	@Test
	public void viewAPTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5618);
		Thread.sleep(4500);
		obj.findNetwork("Open_AP_21P10C69907629", 5618);
		Thread.sleep(3000);
		obj.verifyAP("Open_AP_21P10C69907629", 5618);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5618", data);
		
	}	
	
	//C5617
	@Test
	public void refreshButtonTestAccessPoints() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5617);
		Thread.sleep(4500);
		obj.refreshButton(5617);
		Thread.sleep(2000);
		obj.refreshNotificationAP(5617);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5617", data);
		
	}
	
	//C5590
	@Test
	public void refreshButtonTestClientDevices() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5590);
		Thread.sleep(4500);
		obj.clientDevicesScreen(5590);
		Thread.sleep(3500);
		obj.refreshButton(5590);
		Thread.sleep(2000);
		obj.refreshNotificationClientDevice(5590);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5590", data);
		
	}
	
	//C5592
	@Test
	public void viewDeviceTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5592);
		Thread.sleep(4500);
		obj.clientDevicesScreen(5592);
		Thread.sleep(3500);
		obj.findNetwork("Mohammads-MBP", 5592);
		Thread.sleep(3000);
		obj.verifyDevice("Mohammads-MBP", 5592);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5592", data);
		
	}
	
	//C5619
	@Test
	public void addLocationTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5619);
		Thread.sleep(4500);
		obj.addLocation("Test", 5619);
		Thread.sleep(3000);
		obj.deleteLocation("Test", 5619);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5619", data);
		
	}
	
	//C5620
	@Test
	public void deleteLocationTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5620);
		Thread.sleep(4500);
		obj.addLocation("TestLoc", 5620);
		Thread.sleep(2000);
		obj.deleteLocation("TestLoc", 5620);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5620", data);
		
	}
	
	//C5591
	@Test
	public void clientBlockedListTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5591);
		Thread.sleep(4500);
		obj.clientDevicesScreen(5591);
		Thread.sleep(3500);
		obj.clientBlockedListButton(5591);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5591", data);
		
	}
	
	//C5594
	@Test
	public void verifyDevicesMACField() throws Exception {
		int testId = 5594;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 1, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5595
	@Test
	public void verifyDevicesManufacturerField() throws Exception {
		int testId = 5595;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 2, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5596
	@Test
	public void verifyDevicesIPField() throws Exception {
		int testId = 5596;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 3, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5597
	@Test
	public void verifyDevicesHostNameField() throws Exception {
		int testId = 5597;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 4, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5598
	@Test
	public void verifyDevicesAPField() throws Exception {
		int testId = 5598;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 5, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5599
	@Test
	public void verifyDevicesSSIDField() throws Exception {
		int testId = 5599;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 6, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5600
	@Test
	public void verifyDevicesBandField() throws Exception {
		int testId = 5600;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 7, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5601
	@Test
	public void verifyDevicesSignalField() throws Exception {
		int testId = 5601;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 8, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	//C5602
	@Test
	public void verifyDevicesStatusField() throws Exception {
		int testId = 5602;
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen(testId);
		Thread.sleep(4500);
		obj.clientDevicesScreen(testId);
		Thread.sleep(2500);
		obj.loadAllProfiles(testId);
		obj.verifyNetworkFields(false, "", 9, testId);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
	}
	
	//C5623
	@Test
	public void verifyAPLocationTest() throws Exception {
		Map data = new HashMap();
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen(5623);
		Thread.sleep(4500);
		obj.findNetwork("Open_AP_21P10C69907629", 5623);
		Thread.sleep(3000);
		obj.verifyAPLocation(5623);
		obj.closeBrowser();
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5623", data);
		
	}
}
