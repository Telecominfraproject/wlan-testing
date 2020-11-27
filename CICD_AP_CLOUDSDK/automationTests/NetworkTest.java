package automationTests;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;


class NetworkTest {
	WebDriver driver;
	static APIClient client;
	//static ExtentTest test;
	@BeforeClass
	public static void startTest()
	{
		client = new APIClient("https://telecominfraproject.testrail.com");
		client.setUser("syama.devi@connectus.ai");
		client.setPassword("Connectus123$");
	}
	
	public void launchBrowser() {
		System.setProperty("webdriver.chrome.driver", "/home/netex/nightly_sanity/ui-scripts/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--no-sandbox");
		options.addArguments("--disable-dev-shm-usage");
		options.addArguments("--headless");
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
	
	public void networkScreen() throws InterruptedException {
		driver.findElement(By.linkText("Network")).click();
	}
		
	public void loadAllProfiles() throws InterruptedException {
		while (driver.findElements(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[3]/button/span")).size() != 0) {
			driver.findElement(By.xpath("/html/body/div/section/main/div/div/div[3]/button/span")).click();
			Thread.sleep(2000);	
		}
	}
	
	public void addLocation(String loc) throws InterruptedException {
		try {
			driver.findElement(By.cssSelector(".ant-tree-node-content-wrapper:nth-child(3) > .ant-tree-title > span")).click();
		} catch (Exception E) {
			
			fail("Locations not found");
		}
		
		Thread.sleep(1000);
		
		try {
			driver.findElement(By.xpath("//span[contains(.,'Add Location')]")).click();
		} catch (Exception E) {
			
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
		
		if (driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).getText().equals(loc)) {
			//pass
		} else {
			//System.out.print(driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).getText());
			
			fail("Location could not be added");
		}
	}
	
	public void deleteLocation(String loc) throws InterruptedException {
		driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).click();
		Thread.sleep(1000);
		driver.findElement(By.xpath("//span[contains(.,'Delete Location')]")).click();
		Thread.sleep(2000);
		if (driver.findElement(By.cssSelector(".ant-modal-body > p > i")).getText().equals(loc)) {
			//pass
		} else {
			//System.out.print(driver.findElement(By.cssSelector(".ant-tree-treenode-switcher-close .ant-tree-title > span")).getText());
			
			fail("Location not deleted");
		}
		Actions browser = new Actions(driver);
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.TAB).perform();
		browser.sendKeys(Keys.ENTER).perform();
		Thread.sleep(2000);
		
	}
		
	//Verifies whether profile exists
	public void verifyNetworkFields(boolean expected, String profile, String verifyType) {
		WebElement tbl = driver.findElement(By.xpath("//table"));
		List<WebElement> rows = tbl.findElements(By.tagName("tr"));
		
		//row iteration
		for(int i=0; i<rows.size(); i++) {
		    //check column each in row, identification with 'td' tag
		    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

		    //column iteration
		    for(int j=0; j<cols.size()-1; j++) {
		    	if (cols.get(j).getText().equals(profile) && i!=1) {
		    		if (verifyType.equals("Network")) {
		    			
		    			fail(cols.get(0).getText()+ " has blank fields");
		    		} else {
		    			
		    			fail("MAC: "+ cols.get(1).getText()+ " has blank fields");
		    		}
		    		
		    		
		    	}
		    }
		}
		
	}
	
	//Verifies whether profile exists and clicks
	public void findNetwork(String profile) {
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
		
			fail("Network not found");
		}
		//Assert.assertEquals(false, found);
	}
	
	public void verifyDevice(String profile) {
		try {
			if (driver.findElement(By.cssSelector(".index-module__DeviceDetailCard___2CFDA.ant-card-bordered > div > div > div.index-module__leftWrapContent___2iZZo > p:nth-child(1)")).getText().equals(profile)) {
				//Pass
			}
			else {
				//System.out.print(driver.findElement(By.cssSelector(".index-module__DeviceDetailCard___2CFDA.ant-card-bordered > div > div > div.index-module__leftWrapContent___2iZZo > p:nth-child(1)")).getText());
				
				fail("Wrong profile");
			}
		} catch (Exception E) {
			
			fail("Profile title not found");
		}
	}
	
	public void changeAdvancedSettings() throws InterruptedException {
		driver.findElement(By.cssSelector(".ant-collapse.ant-collapse-icon-position-right > div > div > span")).click();
		Thread.sleep(2000);
		Actions cursor = new Actions(driver);
		driver.findElement(By.xpath("//span[contains(.,'enabled')]")).click();
		cursor.sendKeys(Keys.ARROW_DOWN).perform();
		cursor.sendKeys(Keys.ENTER).perform();
		
		for (int a = 0; a < 50; a++) {
			cursor.sendKeys(Keys.TAB).perform();
			cursor.sendKeys(Keys.ENTER).perform();
			cursor.sendKeys(Keys.ARROW_DOWN).perform();
			cursor.sendKeys(Keys.ENTER).perform();
		}
		
		////////driver.findElement(By.xpath("//button[contains(.,'Save')]")).click();
		
		for (int a = 2; a < 15; a++) {
			if(a == 5 || a== 7 || a == 10 || a == 11 || a == 12){
				  // Will skip all these values.
				  continue;
				}
			
			
			for (int b = 1; b < 4; b++) {
				String elementId = "//*[@id=\"root\"]/section/main/div/div/div[2]/div/form/div[4]/div/div[2]/div/div[" + a + "]/div[2]/div/div/div/div[" + b  + "]/div/div/div/div/div/span[2]";
				WebElement box = driver.findElement(By.xpath(elementId));
				
				if (a == 2 || a== 8 || a == 14) {
					if (!box.getText().equals("disabled")) {
						
						fail("Advanced settings not saved");
					}
				} else if (a == 3){
					if (!box.getText().equals("100")) {
						
						fail("Advanced settings not saved");
					}
				} else if (a == 4 || a == 9){
					if (!box.getText().equals("enabled")) {
						
						fail("Advanced settings not saved");
					}
				} else if (a == 6){
					if (!box.getText().equals("BGN")) {
						
						fail("Advanced settings not saved");
					}
				} else if (a == 13){
					if (!box.getText().equals("20MHz")) {
						
						fail("Advanced settings not saved");
					}
				}
				
			}
		}
		
		if (!driver.findElement(By.id("rtsCtsThresholdis2dot4GHz")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("rtsCtsThresholdis5GHzL")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("rtsCtsThresholdis5GHzU")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxNumClientsis2dot4GHz")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxNumClientsis5GHzL")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxNumClientsis5GHzU")).getAttribute("value").equals("0")) {
			
			fail("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minSignalis2dot4GHz")).getAttribute("value").equals("-50")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minSignalis5GHzL")).getAttribute("value").equals("-50")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minSignalis5GHzU")).getAttribute("value").equals("-50")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdInDBis2dot4GHz")).getAttribute("value").equals("-10")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdInDBis5GHzL")).getAttribute("value").equals("-10")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdInDBis5GHzU")).getAttribute("value").equals("-10")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxApsis2dot4GHz")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxApsis5GHzL")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("maxApsis5GHzU")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdTimeInSecondsis2dot4GHz")).getAttribute("value").equals("120")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdTimeInSecondsis5GHzL")).getAttribute("value").equals("120")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("noiseFloorThresholdTimeInSecondsis5GHzU")).getAttribute("value").equals("120")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("dropInSnrPercentageis2dot4GHz")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("dropInSnrPercentageis5GHzL")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("dropInSnrPercentageis5GHzU")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minLoadFactoris2dot4GHz")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minLoadFactoris5GHzL")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		} else if (!driver.findElement(By.id("minLoadFactoris5GHzU")).getAttribute("value").equals("0")) {
			
			fail ("Advanced settings not saved");
		}
	}
	
	public void verifyAdvancedSettings() throws InterruptedException {
		driver.findElement(By.cssSelector(".ant-collapse.ant-collapse-icon-position-right > div > div > span")).click();
		Thread.sleep(2000);
		
		
		for (int a = 7; a < 13; a++) {
			if(a > 7 && a < 11){
				  // Will skip all these values.
				  continue;
				}
			
			
			for (int b = 1; b < 4; b++) {
				String elementId = "//*[@id=\"root\"]/section/main/div/div/div[2]/div/form/div[4]/div/div[2]/div/div[" + a + "]/div[2]/div/div/div/span[" + b  + "]";
				WebElement box = driver.findElement(By.xpath(elementId));
				
				if (box.getText().equals("")) {
					if (a == 7) {
						
						fail("Mimo Mode field blank");
					} else if (a == 11) {
						
						fail("Active channel field blank");
						
					} else if (a == 12) {
						
						fail("Backup channel field blank");
					}
					
				}
				
			}
		}
		
	}
	
	
	public void verifyAP(String profile) {
		try {
			if (driver.findElement(By.cssSelector("#root > section > main > div > div > div.index-module__mainContent___1X1X6 > div > div.ant-card.ant-card-bordered.ant-card-contain-tabs > div.ant-card-head > div.ant-card-head-wrapper > div.ant-card-head-title > div > div > div:nth-child(1)")).getText().equals(profile)) {
				//Correct profile
			}
			else {
				//System.out.print(driver.findElement(By.cssSelector(".index-module__DeviceDetailCard___2CFDA.ant-card-bordered > div > div > div.index-module__leftWrapContent___2iZZo > p:nth-child(1)")).getText());
				
				fail("Wrong profile");
			}
		} catch (Exception E) {
			
			fail("Profile title not found");
		}
	}
	
	
	public void refreshButton() throws InterruptedException {
		try {
			driver.findElement(By.cssSelector("[title^='reload']")).click();
		} catch (Exception E) {
			
			fail ("Reload button not visible");
		}
		
		Thread.sleep(1000);
	}
	
	
	public void clientBlockedListButton() throws InterruptedException {
		driver.findElement(By.xpath("//span[contains(.,'Blocked List')]")).click();
		Thread.sleep(2000);
		String URL = driver.getCurrentUrl();
		Assert.assertEquals(URL, "https://wlan-ui.qa.lab.wlan.tip.build/system/blockedlist");
		
	}
		
	public void refreshNotificationAP() {
		
		if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Access points reloaded.")) {
			
		} else {
			
			fail("Notification did not appear");
		}
	}
	public void refreshNotificationClientDevice() {
		if (driver.findElement(By.cssSelector(".ant-notification-notice-description")).getText().equals("Client devices reloaded.")) {
			
		} else {
			
			fail("Notification did not appear");
		}
	}
	
	public void clientDevicesScreen() {
		try {
			driver.findElement(By.linkText("Client Devices")).click();
		} catch (Exception E) {
			
			fail("Client Devices tab not visible");
		}
		
	}
	
	@Test
	void verifyFields() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(5000);
		obj.loadAllProfiles();
		obj.verifyNetworkFields(false, "", "Network");
		obj.verifyNetworkFields(false, "N/A", "Network");
		obj.closeBrowser();
		
	}
		
	@Test
	void viewAPTest() throws InterruptedException {
	
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.findNetwork("AP_21P10C69703496_Rashad");
		Thread.sleep(3000);
		obj.verifyAP("AP_21P10C69703496_Rashad");
		obj.closeBrowser();
		
	}	
	
	@Test
	void refreshButtonTestAccessPoints() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.refreshButton();
		Thread.sleep(2000);
		obj.refreshNotificationAP();
		obj.closeBrowser();
		
	}
	@Test
	void refreshButtonTestClientDevices() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.clientDevicesScreen();
		Thread.sleep(3500);
		obj.refreshButton();
		Thread.sleep(2000);
		obj.refreshNotificationClientDevice();
		obj.closeBrowser();
		
	}

	@Test
	void viewDeviceTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.clientDevicesScreen();
		Thread.sleep(3500);
		obj.findNetwork("Mohammads-MBP");
		Thread.sleep(3000);
		obj.verifyDevice("Mohammads-MBP");
		obj.closeBrowser();
		
	}
	@Test
	void addLocationTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.addLocation("Test");
		Thread.sleep(3000);
		obj.deleteLocation("Test");
		obj.closeBrowser();
		
	}
	@Test
	void deleteLocationTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.addLocation("TestLoc");
		Thread.sleep(2000);
		obj.deleteLocation("TestLoc");
		obj.closeBrowser();
		
	}
	@Test
	void clientBlockedListTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.clientDevicesScreen();
		Thread.sleep(3500);
		obj.clientBlockedListButton();
		obj.closeBrowser();
		
	}
	
	@Test
	void verifyDevicesFields() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(2500);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.clientDevicesScreen();
		Thread.sleep(2500);
		obj.loadAllProfiles();
		obj.verifyNetworkFields(false, "", "Device");
		obj.closeBrowser();
		
	}
	
	@Test
	void changeAdvancedSettingsTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.findNetwork("Open_AP_21P10C68712730");
		Thread.sleep(4000);
		obj.verifyAP("Open_AP_21P10C68712730");
		obj.changeAdvancedSettings();
		obj.closeBrowser();
		
	}
	
	@Test
	void verifyAdvancedSettingsTest() throws InterruptedException {
		
		NetworkTest obj = new NetworkTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		obj.networkScreen();
		Thread.sleep(4500);
		obj.findNetwork("Open_AP_21P10C68712730");
		Thread.sleep(4000);
		obj.verifyAP("Open_AP_21P10C68712730");
		obj.verifyAdvancedSettings();
		obj.closeBrowser();
		
	}
	

}
