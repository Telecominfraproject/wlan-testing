package automationTests;

import static org.junit.jupiter.api.Assertions.*;

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
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;


public class DashboardTest {
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
	
	public void networkScreen() throws Exception {
		driver.findElement(By.linkText("Network")).click();
	}
	
	public void clientDevicesScreen() {
		driver.findElement(By.linkText("Client Devices")).click();
	}
	
	public void loadAllProfiles(int testId) throws Exception {
		try {
			while (driver.findElements(By.xpath("//span[contains(.,'Load More')]")).size() != 0) {
				driver.findElement(By.xpath("//span[contains(.,'Load More')]")).click();
				Thread.sleep(2500);	
			}
		}  catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail("Number of AP's provisioned cannot be found");
		}
	
	}
	
	public int verifyAPNumber(int testId) throws MalformedURLException, IOException, APIException {
		
		try {
			String displayed = driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[1]/div[1]/div[2]/div[1]/div[2]")).getText();
			int displ;
			switch(displayed.length()) {
				case 3:
					displ = Integer.parseInt(displayed.substring(displayed.length()-1));
					return displ;
				case 4:
					displ = Integer.parseInt(displayed.substring(displayed.length()-2));
					return displ;
			}
			
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail("Number of AP's provisioned cannot be found");
		}
		return 0;
		
	}
	
	public int verifyDevicesNumber(int testId) throws MalformedURLException, IOException, APIException {
		try {
			String displayed = driver.findElement(By.xpath("//*[@id=\"root\"]/section/main/div/div/div[1]/div[2]/div[2]/div[1]/div[2]")).getText();
			int displ = Integer.parseInt(displayed.substring(displayed.length()-2));
			return displ;
		} catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);

			fail("Number of total devices associated cannot be found");
		}
		return 0;
		
	}
	
	public void verifyGraphs(int testId) throws MalformedURLException, IOException, APIException {
		try {
			
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);

			fail("Number of total devices associated cannot be found");
		}
		List<WebElement> rows = driver.findElements(By.cssSelector("[class^='chart']"));
		List<WebElement> lines = driver.findElements(By.cssSelector("[class^='highcharts-tracker-line']"));
		
		if (lines.size()!= 5) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		Assert.assertEquals("Graphs not displayed", 5, lines.size());
	}
	
	public int countRows(int testId) throws MalformedURLException, IOException, APIException {
		try {
			
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		WebElement tbl = driver.findElement(By.xpath("//table"));
		List<WebElement> rows = tbl.findElements(By.tagName("tr"));
		return rows.size()-2;	
	}
	
	public int findProfile(int testId) throws MalformedURLException, IOException, APIException {
		try {
			
		}catch (Exception E) {
			Map data = new HashMap();
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
		}
		WebElement tbl = driver.findElement(By.xpath("//table"));
		List<WebElement> rows = tbl.findElements(By.tagName("tr"));
		int count = 0;
		
		
		//row iteration
		for(int i=2; i<rows.size(); i++) {
		    //check column each in row, identification with 'td' tag
		    List<WebElement> cols = rows.get(i).findElements(By.tagName("td"));

		    if (!cols.get(7).getText().equals("")) {
		    	count++;
		    }
		    
		}
		return count;
	}
	
	public void verifyDashboardScreenDetails(int testId) throws MalformedURLException, IOException, APIException {		
		Map data = new HashMap();
		try {
			if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div.index-module__infoWrapper___2MqZn > div:nth-child(1) > div.ant-card-head > div > div")).getText().equals("Access Point")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div.index-module__infoWrapper___2MqZn > div:nth-child(2) > div.ant-card-head > div > div")).getText().equals("Client Devices")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div.index-module__infoWrapper___2MqZn > div:nth-child(3) > div.ant-card-head > div > div")).getText().equals("Usage Information (24 hours)")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div:nth-child(2) > div:nth-child(1) > div > div.ant-card-head > div > div.ant-card-head-title")).getText().equals("Inservice APs (24 hours)")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div:nth-child(2) > div:nth-child(2) > div > div.ant-card-head > div > div.ant-card-head-title")).getText().equals("Client Devices (24 hours)")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div:nth-child(2) > div:nth-child(3) > div > div.ant-card-head > div > div.ant-card-head-title")).getText().equals("Traffic (24 hours)")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div:nth-child(3) > div:nth-child(1) > div > div.ant-card-head > div > div")).getText().equals("AP Vendors")) {
				data.put("status_id", new Integer(5));
				data.put("comment", "Fail");
				JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
				fail("Dashboard section not displayed");
			} else if (!driver.findElement(By.cssSelector("#root > section > main > div > div > div:nth-child(3) > div:nth-child(2) > div > div.ant-card-head > div > div")).getText().equals("Client Vendors")) {
				
				fail("Dashboard section not displayed");
			}
		} catch (Exception E) {
			
			data.put("status_id", new Integer(5));
			data.put("comment", "Fail");
			JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/"+testId, data);
			fail("Dashboard section not displayed");
		}
		
	}
	//C5218
	@Test
	public void apDetailsTest() throws Exception {
		Map data = new HashMap();
		DashboardTest obj = new DashboardTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(3000);
		int displayed = obj.verifyAPNumber(5218);
		Thread.sleep(1000);
		obj.networkScreen();
		Thread.sleep(5000);
		obj.loadAllProfiles(5218);
		Thread.sleep(3000);
		int actual = obj.countRows(5218);
		Assert.assertEquals(displayed, actual);
		obj.closeBrowser();
		
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5218", data);
	}
	
	//C5221
	@Test
	public void displayGraphsTest() throws Exception {
		Map data = new HashMap();
		DashboardTest obj = new DashboardTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(5000);
		obj.verifyGraphs(5221);
		Thread.sleep(2000);
		obj.closeBrowser();
		
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5221", data);
		
	}
	
	//C5220
	@Test
	public void displayAllSectionsTest() throws Exception {
		Map data = new HashMap();
		DashboardTest obj = new DashboardTest();
		obj.launchBrowser();
		obj.logIn();
		Thread.sleep(5000);
		obj.verifyDashboardScreenDetails(5220);
		obj.closeBrowser();
		
		data.put("status_id", new Integer(1));
		data.put("comment", "This test worked fine!");
		JSONObject r = (JSONObject) client.sendPost("add_result_for_case/"+runId+"/5220", data);
		
	}

//	@Test
//	void devicesDetailsTest() throws Exception {
//		DashboardTest obj = new DashboardTest();
//		obj.launchBrowser();
//		obj.logIn();
//		Thread.sleep(3000);
//		int displayed = obj.verifyDevicesNumber();
//		Thread.sleep(1000);
//		obj.networkScreen();
//		Thread.sleep(5000);
//		obj.clientDevicesScreen();
//		Thread.sleep(5000);
//		obj.loadAllProfiles();
//		Thread.sleep(1000);
//		int actual = obj.findProfile();
//		Assert.assertEquals(displayed, actual);
//	}
}
