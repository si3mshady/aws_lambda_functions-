  def fill_table_states(self,state):
        try:
            query = "INSERT INTO ec (state) Values(%s)"        
            self.db_cursor.execute(query,(state,))
            self.db_connection.commit()
        except ValueError:
            pass
         

    def fill_table_cases(self,case):
        try:
            case = re.sub(r'[\n\[\]-,]','',str(case))
            query = "INSERT INTO ec (cases) Values(%s)"        
            self.db_cursor.execute(query,(case,))      
            self.db_connection.commit()      
        except Exception as e:
            print(e)
            
    
    def fill_table_fatals(self,rip):
        try:
            rip = re.sub(r'[\n\[\]-,]','',str(rip))
            query = "INSERT INTO ec (fatal) Values(%s)"
            self.db_cursor.execute(query,(rip,))
            self.db_connection.commit()      
        except Exception as e:
            print(e)
        
    
    def fill_table_recovered(self,val):
        try:
            val = re.sub(r'[\n\[\]-,]','',str(val))
            query = "INSERT INTO ec (recovered) Values(%s)"
            self.db_cursor.execute(query,(val,))
            self.db_connection.commit()      
        except Exception as e:
            print(e)