workspace {
  model {

    enterprise "BambooConnect" {

      # This may be sub-divided into multiple agents (based on their roles)
      # e.g. Pre-sales agent, Sales agent
      agent = person "Developer" {
        description "A developer who wants to use the BambooConnect Library"
          tags "Existing"
      }

      bamboo_system = softwareSystem "Bamboo Connect Library" {
        description "The system that provides ETL functinoality"
        #tags "mvp" "new system"
        #!docs docs

          extractrors = container "Extractors" {
            description "Extractors: Support the easy extract of data"
          }

          transformers = container "Transformers" {
            description "Provides functionality to transform data"
          }

          loaders = container "Loaders" {
            description "Provides the ability to load the transformed data back into a system"
          }

          support = container "Support" {
            description "Support Tools to easily do common tasks. No external dependencies"

            auth_support = component "Authenticaion Support"
          }

          support -> loaders

      # #bamboo_system

        google_sheets = container "Google Sheet" {
          description "Where data is stored prior to and maybe after ETL"
          technology "Google Sheets"
        }
        jira = container "JIRA" {
          description "External JIRA system that can be queried"
          technology "JIRA"
        }
        google_drive = container "Google Drive" {
          description "External system to save/load files"
          technology "Google Drive"
        }
        jira_obss = container "JIRA OBSS Lead/Cycle Time Plugin" {
          description "External JIRA system that can be queried"
          technology "JIRA OBSS"
        }
      }

      sample_bamboo_app = softwareSystem "Sample System That Uses Bamboo Library" {
        description "An example of a system that calls the Bamboo Library. It initiates and then runs through the ETL"
        tags "mvp"
      }
      sample_bamboo_app -> bamboo_system "uses"
    } #bamboo_system


    customer = person "Customer" {
      description "A user registered with UB Partner that is interested in getting their tax declaration done by UB Partner"
      tags "Customer"
    }
  }

  views {
    theme default

    systemLandscape "SystemLandscape" {
      include *
      autoLayout
    }

    systemContext bamboo_system "SystemContext" {
      include *
      autoLayout
    }

    container bamboo_system sample_bamboo_app "Container Diagram" {
      include * backend_group
      autolayout
    }

    styles {
      # A container that runs on a mobile devices such as a phone or tablet.
      element "Mobile App" {
        shape MobileDevicePortrait
      }

      # A container for Database
      element "Database" {
        shape Cylinder
      }

      # A container for Blob storage
      element "Bucket" {
        shape Folder
      }

      # A system that is included for understanding but is not actually part of our scope
      element "Peripheral System" {
        background 	#6A6C6E
      }

      # Browser based application
      element "WebApp" {
        shape WebBrowser
      }

      # Sub-component of application
      element "Component" {
        shape Component
      }

      element "Group" {
          color #ff0000
          strokeWidth 2
      }
    }

    !plugin com.structurizr.dsl.plugins.mermaid.MermaidEncoderPlugin {
      "mermaid.url" "http://localhost:3000"
    }
  }
}
